#############################################################################
#
#
# Module of BFA that reads and manages bf-xml 1.1 mainly for the master
#
#
#############################################################################
""" This module does parsing of the event log for the master server.

    Dependencies:

        bfassist <- (references.)eventlogs
            |
            \-> bfa_logging
             -> master -> league @parseRoundStats

        note::  Author(s): Mitch last-check: 07.07.2021 """

from datetime import datetime, timedelta
from pathlib import Path

from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


current_round = None
eventLogCreation = None
players = {}


def parse(inXML: str):
    """ Main function of this module that delegates parsing using the tag list.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    log("Parsing inXML for server.", 0)
    for tag in tagList:
        if tag in inXML:
            tagList[tag][0](inXML)


def initialiseCurrentRound(inXML: str = None):
    """ Simple function to initialise current round variable with default value.

            note::  Author(s): Mitch """

    global current_round

    if inXML is not None:
        startOffset = timedelta(seconds=float(inXML.split("\"")[1]))
        # noinspection PyTypeChecker
        start = eventLogCreation + startOffset
    else:
        start = eventLogCreation

    current_round = {
        'server': {
            'BFAName': "",
            'binaries': {
                "Name": "",
                'Digest': ""
            },
            'Ip': "",
            'GamePort': "",
            'LocalUP': False,
            'hasHenkPatch': {
                "teleportation": False,
                "listPlayersMods": False
            }
        },
        'settings': {},
        'results': {},
        'Start': str(start),
        'End': None,
        'Winner': None,
        'VType': None,
        'TicketsAxis': None,
        'TicketsAllies': None
    }


def parseRound(inXML: str):
    """ Function to parse BfRound-xml start.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    global current_round, eventLogCreation

    initialiseCurrentRound(inXML)
    log("Adding a BfRound.", 1)


def parseRoundStats(inXML: str):
    """ Function to parse BfRoundStats-xml.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    from bfassist.master.league import LeagueRound

    global current_round, eventLogCreation, players

    log("Parsing RoundStats.", 1)
    inlines = inXML.split('\n')
    player_id = ''
    if current_round is None:
        initialiseCurrentRound()

    for line in inlines:
        if "<bf:roundstats timestamp=\"" in line:

            # If we missed the start of the round, fill eventlogcreate
            # The match history for the server could then be either empty
            endOffset = timedelta(seconds=float(line.split("\"")[1]))
            # noinspection PyTypeChecker
            current_round['End'] = str(eventLogCreation + endOffset)
        elif "<bf:winningteam" in line:
            current_round['Winner'] = line.split('>')[1].split('<')[0]
        elif "<bf:victorytype" in line:
            current_round['VType'] = line.split('>')[1].split('<')[0]
        elif "<bf:teamtickets team=\"1\"" in line:
            current_round['TicketsAxis'] = getXMLFeat(line, '1')
        elif "<bf:teamtickets team=\"2\"" in line:
            current_round['TicketsAllies'] = getXMLFeat(line, '2')
        elif "<bf:playerstat" in line:
            player_id = int(line.split("\"")[1])
            current_round['results'][player_id] = {
                'PlayerId':             player_id,
                'Keyhash':              players[player_id],
                'NameAtEnd':            "",
                'IsAi':                 None,
                'TeamAtEnd':            None,
                'Score':                None,
                'Kills':                None,
                'Deaths':               None,
                'TeamKills':            None,
                'Captures':             None,
                'Attacks':              None,
                'Defences':             None,
                'Objectives':           None,
                'ObjectiveTeamKills':   None
            }

        elif "<bf:statparam name=\"player_name\"" in line:
            current_round['results'][player_id]['NameAtEnd'] = getXMLFeat(line, 'player_name')
        elif "<bf:statparam name=\"is_ai\"" in line:
            current_round['results'][player_id]['IsAi'] = getXMLFeat(line, 'is_ai')
        elif "<bf:statparam name=\"team\"" in line:
            current_round['results'][player_id]['TeamAtEnd'] = getXMLFeat(line, 'team')
        elif "<bf:statparam name=\"score\"" in line:
            current_round['results'][player_id]['Score'] = getXMLFeat(line, 'score')
        elif "<bf:statparam name=\"kills\"" in line:
            current_round['results'][player_id]['Kills'] = getXMLFeat(line, 'kills')
        elif "<bf:statparam name=\"deaths\"" in line:
            current_round['results'][player_id]['Deaths'] = getXMLFeat(line, 'deaths')
        elif "<bf:statparam name=\"tks\"" in line:
            current_round['results'][player_id]['TeamKills'] = getXMLFeat(line, 'tks')
        elif "<bf:statparam name=\"captures\"" in line:
            current_round['results'][player_id]['Captures'] = getXMLFeat(line, 'captures')
        elif "<bf:statparam name=\"attacks\"" in line:
            current_round['results'][player_id]['Attacks'] = getXMLFeat(line, 'attacks')
        elif "<bf:statparam name=\"defences\"" in line:
            current_round['results'][player_id]['Defences'] = getXMLFeat(line, 'defences')
        elif "<bf:statparam name=\"objectives\"" in line:
            current_round['results'][player_id]['Objectives'] = getXMLFeat(line, 'objectives')
        elif "<bf:statparam name=\"objectivetks\"" in line:
            current_round['results'][player_id]['ObjectiveTeamKills'] = getXMLFeat(line, 'objectivetks')
        elif "</bf:roundstats>" in line:
            # noinspection PyTypeChecker
            LeagueRound.fromDict(current_round)

            current_round = None


def parseServerSettings(inXML: str):
    """ Function to parse BfSettings-xml.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    global current_round

    if current_round is None:
        initialiseCurrentRound()

    current_round['settings'] = {
                        'ServerName': getXMLFeat(inXML, 'server name'), 'GamePort': getXMLFeat(inXML, 'port'),
                        'Dedicated': getXMLFeat(inXML, 'dedicated'), 'ModId': getXMLFeat(inXML, 'modid'),
                        'MapId': getXMLFeat(inXML, 'mapid'), 'Map': getXMLFeat(inXML, 'map'),
                        'GameMode': getXMLFeat(inXML, 'game mode'), 'GameTime': getXMLFeat(inXML, 'gametime'),
                        'MaxPlayers': getXMLFeat(inXML, 'maxplayers'), 'ScoreLimit': getXMLFeat(inXML, 'scorelimit'),
                        'NoRounds': getXMLFeat(inXML, 'norounds'), 'SpawnTime': getXMLFeat(inXML, 'spawntime'),
                        'SpawnDelay': getXMLFeat(inXML, 'spawndelay'),
                        'GameStartDelay': getXMLFeat(inXML, 'gamestartdelay'),
                        'RoundStartDelay': getXMLFeat(inXML, 'roundstartdelay'),
                        'SoldierFf': getXMLFeat(inXML, 'soldierff'), 'VehicleFf': getXMLFeat(inXML, 'vehicleff'),
                        'TicketRatio': getXMLFeat(inXML, 'ticketratio'), 'Internet': getXMLFeat(inXML, 'internet'),
                        'AlliedTr': getXMLFeat(inXML, 'alliedtr'), 'AxisTr': getXMLFeat(inXML, 'axistr'),
                        'CoopSkill': getXMLFeat(inXML, 'coopskill'), 'CoopCpu': getXMLFeat(inXML, 'coopcpu'),
                        'ReservedSlots': getXMLFeat(inXML, 'reservedslots'),
                        'AllowNoseCam': getXMLFeat(inXML, 'allownosecam'),
                        'FreeCamera': getXMLFeat(inXML, 'freecamera'),
                        'ExternalViews': getXMLFeat(inXML, 'externalviews'),
                        'AutoBalance': getXMLFeat(inXML, 'autobalance'),
                        'TagDistance': getXMLFeat(inXML, 'tagdistance'),
                        'TagDistanceScope': getXMLFeat(inXML, 'tagdistancescope'),
                        'KickBack': getXMLFeat(inXML, 'kickback'),
                        'KickBackSplash': getXMLFeat(inXML, 'kickbacksplash'),
                        'SoldierFfOnSplash': getXMLFeat(inXML, 'soldierffonsplash'),
                        'VehicleFfOnSplash': getXMLFeat(inXML, 'vehicleffonsplash'),
                        'HitIndication': getXMLFeat(inXML, 'hitindication'), 'TkPunish': getXMLFeat(inXML, 'tkpunish'),
                        'CrossHairPoint': getXMLFeat(inXML, 'crosshairpoint'),
                        'DeathCamType': getXMLFeat(inXML, 'deathcamtype'),
                        'ContentCheck': getXMLFeat(inXML, 'contentcheck'),
                        'Sv_Punkbuster': getXMLFeat(inXML, 'sv_punkbuster')
    }

    current_round['server']['BFAName'] = current_round['settings']['ServerName']
    current_round['server']['Ip'] = current_round['server']['BFAName']
    current_round['server']['GamePort'] = current_round['settings']['GamePort']


# noinspection PyUnusedLocal
def parseCreatePlayer(inXML: str):
    """ Function to parse BfCreatePlayer-xml.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    pass


# noinspection PyUnusedLocal
def parseKeyHash(inXML: str):
    """ Function to parse BfKeyhash-xml.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    global players

    player_id = int(getXMLFeat(inXML, 'player_id'))
    player_keyhash = getXMLFeat(inXML, 'keyhash')
    players[player_id] = player_keyhash


# noinspection PyUnusedLocal
def parseSpawnEvent(inXML: str):
    """ Function to parse BfSpawnEvent-xml.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    pass


# noinspection PyUnusedLocal
def parseDestroyPlayer(inXML: str):
    """ Function to parse BfDestroyPlayer-xml.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    pass


# noinspection PyUnusedLocal
def parseChatMessage(inXML: str):
    """ Function to parse BfChatMessage-xml.

        :param inXML:       The xml to be processed.

            note::  Author(s): Mitch """

    pass


def getXMLFeat(inXML: str, inFeat: str):
    """ Function to parse BfCreatePlayer-xml looking for a certain feature value.

            :param inXML:   The xml to be processed.
            :param inFeat:  The feature we're looking for.
            :return:        The extracted value of the feature. None if none.

                note::  Author(s): Mitch """

    if "\">" in inXML:
        content = inXML.split(inFeat + '\">')[1].split('<')[0]
        if contest.isdigit():
            return int(content)
        else:
            return content
    else:
        return None


def importEventLog(inPath: str):
    """ Function to read an event log indirectly from a file when transmission of data was missed.

        :param inPath:      Path to the xml file containing the event logs.

            note::  Author(s): Mitch """

    global eventLogCreation, players

    eventLogCreation = datetime.fromtimestamp(Path(inPath).stat().st_ctime)

    log("Trying to import an event log.")
    with open(inPath, 'r', encoding='latin_1') as importfile:
        for line in importfile:
            if '</bf:log>' in line:
                log("Finished reading a full event log section.")
            elif '<bf:round time' in line:
                paragraph = line
                parse(paragraph)
            elif '<bf:server' in line:
                paragraph = line
                while '</bf:server' not in line:
                    if '</bf:log>' in line:
                        log("Finished reading a full event log section.")
                    else:
                        paragraph += line
                        line = next(importfile)
                paragraph += line
                parse(paragraph)
            elif '<bf:event' in line:
                paragraph = line
                while '</bf:event' not in line:
                    if '</bf:log>' in line:
                        log("Finished reading a full event log section.")
                    else:
                        paragraph += line
                        line = next(importfile)
                paragraph += line
                parse(paragraph)
            elif '<bf:roundstats' in line:
                paragraph = line
                while '</bf:roundstats' not in line:
                    if '</bf:log>' in line:
                        log("Finished reading a full event log section.")
                    else:
                        paragraph += line
                        line = next(importfile)
                paragraph += line
                parse(paragraph)

    log("Finished reading a full event log import.", 2)
    eventLogCreation = None
    players = {}
    return True


def importLogs():
    """ Function that imports all event log files placed in the import folder.

            note::  Author(s): Mitch """

    for eventLog in listdir('bfassist/references/eventlogs/import'):
        importEventLog('bfassist/references/eventlogs/import/' + eventLog)


tagList = {
    '<bf:event name=\"chat\"':              [parseChatMessage],
    '<bf:event name=\"createPlayer\"':      [parseCreatePlayer],
    '<bf:event name=\"playerKeyHash\"':     [parseKeyHash],
    '<bf:event name=\"disconnectPlayer\"':  [parseDestroyPlayer],
    '<bf:event name=\"spawnEvent\"':        [parseSpawnEvent],
    '<bf:server':                           [parseServerSettings],
    '<bf:round ':                           [parseRound],
    '<bf:roundstats':                       [parseRoundStats]
}
