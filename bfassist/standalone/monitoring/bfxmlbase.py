#############################################################################
#
#
# Module of BFA that reads and manages bf-xml 1.1
#
#
#############################################################################
""" This module does most of the parsing of the event log.

    Dependencies:

        2nd-party dependency numpy

            bfassist <- standalone <- monitoring <- bfxmlbase
                |           |           \
                |           \            -> logreader
                |            -> monitoring
                \-> bfa_logging
                 -> network -> client   @LogReaderParsing.parseRoundStats

        note::  Author(s): Mitch, henk last-check: 08.07.2021 """

from datetime import timedelta
from html import unescape

from numpy import fromstring

from bfassist.standalone.monitoring.logreader import *
from bfassist.standalone.monitoring import RealTimeEvent, RealTimeRound, BfServerSettings, BfServerSetting,\
                                           BfPlayerRound
from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class LogReaderParsing(LogReader):
    """ Extension of the log reader that does most of the actual parsing.

            note::  Author(s): Mitch """

    def __init__(self, server: Server):
        super().__init__(server)

        self.realTimeRound = self.server.StatsInterface.realTimeRound

    def parseEvent(self, inXML: str):
        """ Function to parse BfEvent-xml.

            :param inXML:   The xml to be processed.

                note::  Author(s): Mitch """

        eventName, timeStamp, inXML = self.getNameAndTimeStamp(inXML)
        event = RealTimeEvent(eventName)
        event.parameters = self.getAllXMLParameters(inXML)
        if timeStamp in self.realTimeRound.eventDict:
            self.realTimeRound .eventDict[timeStamp].append(event)
        else:
            self.realTimeRound .eventDict[timeStamp] = [event]
        if eventName in self.hooks:
            try:
                super().hooks[eventName](event)
            except KeyError:
                log("Seems like we couldn't find a player by their id.", 3)
    super().tagList[event_starts] = parseEvent

    def parseRound(self, inXML: str):
        """ Function to parse BfRound-xml start.

            :param inXML:   The xml to be processed.

                note::  Author(s): Mitch """

        self.server.StatsInterface.realTimeRound = RealTimeRound(self.server)
        self.realTimeRound = self.server.StatsInterface.realTimeRound

        startOffset = timedelta(seconds=float(inXML.split("\"")[1]))
        start = self.server.MonitoringInterface.creationTimeLastLog + startOffset

        self.realTimeRound.roundStats.setStart(start)
        log("Adding a BfRound.", 1)
    super().tagList[round_starts] = parseRound

    def parseRoundStats(self, inXML: str):
        """ Function to parse BfRoundStats-xml.

            :param inXML:   The xml to be processed.

                note::  Author(s): Mitch """

        log("Parsing RoundStats for a server.", 1)
        inLines = inXML.splitlines()

        while inLines:
            line = inLines.pop(0).strip()
            if line.startswith(roundstats_end):
                self.realTimeRound.roundStats.setResultIds(
                    set(str(playerRound.getPlayerRoundId())
                        for playerRound in self.realTimeRound.roundStats.results.values())
                )

                if self.realTimeRound.liveRound:
                    from bfassist.network.client import BFA_CLIENT
                    BFA_CLIENT.updateLeaguePlayers(self.server.PlayerInterface.onlinePlayerWithId)
                    self.realTimeRound.roundStats.sendToMaster()
                    self.realTimeRound.liveRound = False

                self.server.StatsInterface.realTimeRound = None
                self.realTimeRound = self.server.StatsInterface.realTimeRound
            elif line.startswith('<bf:playerstat'):
                currentPlayer_id = int(line[line.find('"'):line.rfind('"')])
                inLines = self.parsePlayerStat(currentPlayer_id, inLines)
            elif line.startswith('<bf:teamtickets team="2"'):
                self.realTimeRound.roundStats.setTicketsAllies(self.getInnerXML(line))
            elif line.startswith('<bf:teamtickets team="1"'):
                self.realTimeRound.roundStats.setTicketsAxis(self.getInnerXML(line))
            elif line.startswith('<bf:victorytype'):
                self.realTimeRound.roundStats.setVType(self.getInnerXML(line))
            elif line.startswith('<bf:winningteam'):
                self.realTimeRound.roundStats.setWinner(self.getInnerXML(line))
    super().tagList[roundstats_start] = parseRoundStats

    def parseServerSettings(self, inXML: str):
        """ Function to parse BfSettings-xml.

            :param inXML:   The xml to be processed.

                note::  Author(s): Mitch """

        inLines = inXML.splitlines()

        settings = ['ServerName', 'GamePort', 'Dedicated', 'ModId', 'MapId', 'Map', 'GameMode', 'GameTime',
                    'MaxPlayers', 'ScoreLimit', 'NoRounds', 'SpawnTime', 'SpawnDelay', 'GameStartDelay',
                    'RoundStartDelay', 'SoldierFf', 'VehicleFf', 'TicketRatio', 'Internet', 'AlliedTr', 'AxisTr',
                    'CoopSkill', 'CoopCpu', 'ReservedSlots', 'AllowNoseCam', 'FreeCamera', 'ExternalViews',
                    'AutoBalance',  'TagDistance', 'TagDistanceScope', 'KickBack', 'KickBackSplash',
                    'SoldierFfOnSplash', 'VehicleFfOnSplash', 'HitIndication', 'TkPunish', 'CrossHairPoint',
                    'DeathCamType', 'ContentCheck', 'Sv_Punkbuster']

        current_settings = {}
        for x in range(len(inLines)):
            current_settings[settings[x]] = self.getInnerXML(inLines[x])

        if BfServerSettings.exists(current_settings) and \
                BfServerSettings.getWithoutIdByFullDefinition(current_settings).getSettingsId() != \
                self.realTimeRound.roundStats.settings.getSettingsId():
            self.realTimeRound.roundStats.settings = BfServerSetting.getWithoutIdByFullDefinition(current_settings)
        elif not self.realTimeRound.roundStats.settings.storageDict.exists(current_settings):
            self.realTimeRound.roundStats.settings = BfServerSetting(*current_settings.values())

        self.server.SettingsInterface.settings = self.realTimeRound.roundStats.settings
    super().tagList[server_starts] = parseServerSettings

    def parsePlayerStat(self, player_id: int, inLines: list):
        """ Function that parses a complete set of playerstat for a given player_id and excerpt of roundstats that begin
        with the first line of the playerstat to parse.

            :param player_id:   The id of the player this playerstat belongs to.
            :param inLines:     The excerpt of roundstats.

            :return:            The rest of the roundstats.

                note::  Author(s): Mitch """

        player = self.server.PlayerInterface.onlinePlayerWithId[player_id]
        if player is None:
            log("Whoops we couldn't find a player we were supposed to have tracked. " + "\n".join(inLines)
                + " id " + str(player_id) + " not in " + str(self.server.PlayerInterface.onlinePlayerWithId), 4)
        else:
            self.realTimeRound.roundStats.results[player_id] = BfPlayerRound(self.realTimeRound.roundStats.getRoundId(),
                                                                             player_id, player.getKeyhash())
        self.realTimeRound.roundStats.results[player_id].setNameAtEnd(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setIsAi(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setTeamAtEnd(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setScore(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setKills(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setDeaths(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setTeamKills(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setCaptures(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setAttacks(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setDefences(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setObjectives(self.getInnerXML(inLines.pop(0)))
        self.realTimeRound.roundStats.results[player_id].setObjectiveTeamKills(self.getInnerXML(inLines.pop(0)))

        return inLines[1:]

    @staticmethod
    def getNameAndTimeStamp(inXML: str):
        """ Function to parse and extract the event name and timestamp of a log-entry.

                :param inXML:   The xml to be processed.

                :return:        A triple containing the name and timestamp of the event and the remaining xml.

                    note::  Author(s): Mitch """

        eventNameStart = inXML.find("name=\"")
        if eventNameStart != -1:
            inXML = inXML[eventNameStart + len("name=\""):]
            eventNameEnd = inXML.find("\"")
            eventName = inXML[:eventNameEnd]
            inXML = inXML[eventNameEnd + 1:]
        else:
            eventName = None

        timeStampStart = inXML.find("timestamp=\"")
        if timeStampStart != -1:
            inXML = inXML[timeStampStart + len("timestamp=\""):]
            timeStampEnd = inXML.find("\"")
            timeStamp = inXML[:timeStampEnd]
            inXML = inXML[timeStampEnd + 1:]
        else:
            timeStamp = None

        return eventName, timeStamp, inXML

    def getAllXMLParameters(self, inXML: str):
        """ Function to parse Bf-xml looking for all parameters and their values.

            :param inXML:   The xml to be processed.

            :return:        A dictionary containing the parameter names as keys and their values as values.

                note::  Author(s): Mitch """

        params = {}

        paramStart = inXML.find("<bf:param ")
        while paramStart != -1:
            inXML = inXML[paramStart + len("<bf:param "):]
            typeStart = inXML.find("type=\"")
            inXML = inXML[typeStart + len("type=\""):]
            typeEnd = inXML.find("\"")
            Type = inXML[:typeEnd]
            paramStart = inXML.find("name=\"")
            inXML = inXML[paramStart + len("name=\""):]
            paramEnd = inXML.find("\"")
            params[inXML[:paramEnd]] = self.importParamFromString(unescape(inXML[paramEnd + 2:inXML.find("<")]), Type)
            paramStart = inXML.find("<bf:param ")

        return params

    @staticmethod
    def getInnerXML(inXML: str):
        """ Simple function to get the inner content of a line of bf-xml.

            :param inXML:   The xml to be processed.

            :return:        The value inside the xml. (If it is a digit it will be cast to int)

                note::  Author(s): Mitch """

        value = inXML[inXML.find('>') + 1:inXML.rfind('<')]
        if value.isdigit():
            return int(value)
        else:
            return value

    @staticmethod
    def importParamFromString(inParam: str, inType: str):
        """ Function that imports a parameter from string and casts it to its corresponding type.

            :param inParam: The value of the parameter as string.
            :param inType:  The type of the parameter.

            :return:        The parameter having its corresponding type.

                note::  Author(s): Mitch, henk """

        if inType == 'int':
            return int(inParam)
        elif inType == 'vec3':
            if inType == '(unknown)':
                return None
            else:
                return fromstring(inParam, dtype=float, sep='/')
        elif inType == 'string':
            return inParam


LogReader = LogReaderParsing
