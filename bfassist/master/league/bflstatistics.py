#############################################################################
#
#
# Module of BFA that manages league activity concerning players
#
#
#############################################################################
""" This module should introduce functionality related to league activity. Especially such that is closely related to
statistics.

    Dependencies:

        bfassist <- (master.league.)bflstatistics
            |
            |-> references -> eventlogs
            \-> sql
             -> master -> league

        note::  Author(s): Mitch last-check: 07.07.2021 """

from datetime import datetime
from os import listdir

from bfassist.references.eventlogs import importEventLog, importLogs
from bfassist.sql import *
from bfassist.master.league import LeagueServers, ServerBinaries, ServerSettings, BfServerBinary, BfServer, \
                                   BfServerSetting


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BfPlayerRound(DBStorable, table="playerroundstats", live=False):
    """ A BfPlayerRound is supposed to correspond to the global bfa perspective of a player round on a bfa client.

        :param PlayerRoundId:       Identifier of the stats of this player in this particular round.
        :param RoundId:             Identifier of this particular round.
        :param PlayerId:            Id of the player on the server.
        :param Keyhash:             Keyhash.
        :param NameAtEnd:           Name after the round finished.
        :param IsAi:                Is a bot.
        :param TeamAtEnd:           The team the player finished on.
        :param Score:               Score.
        :param Kills:               Kills.
        :param Deaths:              Deaths.
        :param TeamKills:           Team kills.
        :param Captures:            Captures (CTF).
        :param Attacks:             Attacks (CTF).
        :param Defences:            Defences (CTF).
        :param Objectives:          Objective kills.
        :param ObjectiveTeamKills:  Objective team kills.

            note::  Author(s): Mitch """

    def __init__(self, RoundId: int, PlayerId: int, Keyhash: str, NameAtEnd: str, IsAi: int, TeamAtEnd: int, Score: int,
                 Kills: int, Deaths: int, TeamKills: int, Captures: int, Attacks: int, Defences: int, Objectives: int,
                 ObjectiveTeamKills: int, PlayerRoundId: int = None):
        self.SPlayerRoundId = PlayerRoundId, INTEGER, PRIMARY_KEY
        self.SRoundId = RoundId, INTEGER
        self.SPlayerId = PlayerId, INT
        self.SKeyhash = Keyhash, VARCHAR(32)
        self.SNameAtEnd = NameAtEnd, VARCHAR(32)
        self.SIsAi = IsAi, BIT
        self.STeamAtEnd = TeamAtEnd, BIT
        self.SScore = Score, SMALLINT
        self.SKills = Kills, SMALLINT
        self.SDeaths = Deaths, SMALLINT
        self.STeamKills = TeamKills, SMALLINT
        self.SCaptures = Captures, SMALLINT
        self.SAttacks = Attacks, SMALLINT
        self.SDefences = Defences, SMALLINT
        self.SObjectives = Objectives, SMALLINT
        self.SObjectiveTeamKills = ObjectiveTeamKills, SMALLINT

        self.insertToDB()

    @classmethod
    def fromDict(cls, roundDict: dict):
        return cls(RoundId=roundDict['RoundId'], PlayerId=roundDict['PlayerId'], Keyhash=roundDict['Keyhash'],
                   NameAtEnd=roundDict['NameAtEnd'], IsAi=roundDict['IsAi'], TeamAtEnd=roundDict['TeamAtEnd'],
                   Score=roundDict['Score'], Kills=roundDict['Kills'], Deaths=roundDict['Deaths'],
                   TeamKills=roundDict['TeamKills'], Captures=roundDict['Captures'], Attacks=roundDict['Attacks'],
                   Defences=roundDict['Defences'], Objectives=roundDict['Objectives'],
                   ObjectiveTeamKills=roundDict['ObjectiveTeamKills'])


BfPlayerRounds = BfPlayerRound.storageDict


class LeagueRound(DBStorable, table="roundstats", live=False):
    """ A league round is supposed to correspond to a bf round that's adjusted to bf league purposes.

        :param server:          A global bfa server representation.
        :param settings:        A global bfa server settings representation.
        :param results:         A dictionary of global bfa player round stats representations with round player ids as
                                keys and the global bfa player round stat representations as values.

        :param RoundId:         The identifier of this particular round in the database.
        :param Start:           Datetime of the start of the round.
        :param End:             Datetime of the end of the round.
        :param Winner:          The winner of the round according to what bf considers winner.
        :param VType:           The victory type achieved according to bf.
        :param TicketsAxis:     Axis tickets at the end of the round.
        :param TicketsAllies:   Allied tickets at the end of the round.

        :param ServerId:        Id of the corresponding global bfa server object.
        :param ResultIds:       Id of all corresponding global bfa player round stats objects contained.
        :param SettingsId:      Id of the corresponding global bfa server settings object.

            ::important:: Usually assuming 200 tickets per side since we're not keeping track of the specific map
            settings as of now. Also we discount disconnected scores if live round functionality isn't used.
            note::  Author(s): Mitch """

    def __init__(self, Start: datetime, End: datetime, Winner: int, VType: int, TicketsAxis: int, TicketsAllies: int,
                 ServerId: str = None, ResultIds: set = None, SettingsId: int = None, RoundId: int = None,
                 server: dict = None, settings: dict = None, results: dict = None):

        if server and server['Ip'] + ':' + server['GamePort'] in LeagueServers:
            self.server = LeagueServers[server['Ip'] + ':' + server['GamePort']]
            if self.server.getBFAName() != server['BFAName']:
                self.server.setBFAName(server['BFAName'])
            if self.server.getLocalUP() != server['LocalUP']:
                self.server.setLocalUP(server['LocalUP'])
            if self.server.getBinaryDigest() != server['binaries']['Digest']:
                if server['binaries']['Digest'] in ServerBinaries:
                    self.server.setBinaryDigest(ServerBinaries[server['binaries']['Digest']])
                else:
                    BfServerBinary.fromDict(server['binaries'])
        else:
            self.server = BfServer.fromDict(server)

        if settings and ServerSettings.exists(settings):
            self.settings = ServerSettings.getWithoutIdByFullDefinition(settings)
        else:
            self.settings = BfServerSetting.fromDict(settings)

        self.SRoundId = RoundId, INTEGER, PRIMARY_KEY

        self.SStart = Start, DATETIME
        self.SEnd = End, DATETIME
        self.SWinner = Winner, BIT
        self.SVType = VType, TINYINT
        self.STicketsAxis = TicketsAxis, SMALLINT
        self.STicketsAllies = TicketsAllies, SMALLINT

        if ServerId:
            self.SServerId = ServerId, INTEGER
        else:
            self.SServerId = self.server.getAddress(), INTEGER

        if ResultIds:
            self.SResultIds = ResultIds, TEXT
        else:
            self.SResultIds = set(), TEXT

        if SettingsId:
            self.SSettingsId = SettingsId, INTEGER
        else:
            self.SSettingsId = self.settings.getSettingsId(), INTEGER

        self.insertToDB()

        if results:
            for player_id in results:
                results[player_id].update({'RoundId': self.getRoundId()})
                results[player_id] = BfPlayerRound.fromDict(results[player_id])
            self.results = results
            self.setResultIds(set(str(result.getPlayerRoundId()) for result in self.results.values()))
        else:
            self.results = {}

    @classmethod
    def fromDict(cls, roundDict: dict):
        return cls(server=roundDict['server'], settings=roundDict['settings'], results=roundDict['results'],
                   Start=datetime.strptime(roundDict['Start'], '%Y-%m-%d %H:%M:%S.%f'),
                   End=datetime.strptime(roundDict['End'], '%Y-%m-%d %H:%M:%S.%f'), Winner=roundDict['Winner'],
                   VType=roundDict['VType'], TicketsAxis=roundDict['TicketsAxis'],
                   TicketsAllies=roundDict['TicketsAllies'])

    @staticmethod
    def filterLogs():
        """ Function that filters the stored logs to exclude obviously faulty ones.

        Filter conditions:
        (0)     If there were no livePlayers it is faulty.
        (1)     If a round lasted for less than 3 minutes it should be faulty.
        (2)     If both teams lost no more than a total of 50 tickets (assuming both teams start with 200 tickets) it
                should be faulty.
        (3)     If either team has a negative total score or more than 2 livePlayers on either team have a negative
                score then it should be faulty.
        (4)     If there were less than 6 livePlayers on one side or less than 12 livePlayers in total then it should be
                faulty.

                note::  Author(s): Mitch """

        for leagueRound in LeagueRound.storageDict:
            if leagueRound.getResultIds() != {''}:
                if leagueRound.getDuration() < 180:
                    leagueRound.delete()
                elif leagueRound.getTicketsAllies() + leagueRound.getTicketsAxis() > 400 - 50:
                    leagueRound.delete()
                elif leagueRound.getScoreAllies() < 0 or leagueRound.getScoreAxis() < 0 or \
                        leagueRound.getNumberOfNegativeScoresAllies() > 2 or \
                        leagueRound.getNumberOfNegativeScoresAxis() > 2:
                    leagueRound.delete()
                elif leagueRound.countAllies() < 6 or leagueRound.countAxis() < 6 or \
                        leagueRound.countAxis() + leagueRound.countAllies() < 12:
                    leagueRound.delete()
            else:
                leagueRound.delete()

    def delete(self):
        """ Function that overrides the delete function and deletes a league round as well as the bf player rounds
        linked to it in other tables.

            note::  Author(s): Mitch """

        if self.getResultIds() != {''}:
            for resultId in self.getResultIds():
                BfPlayerRounds[int(resultId)].delete()
        super().delete()

    def getDuration(self):
        """ Function that calculates the duration of the round in seconds.

            :return:    Number of seconds this round lasted.

                note::  Author(s): Mitch """

        return (self.getEnd() - self.getStart()).total_seconds()

    def getScoreAllies(self):
        """ Function that calculates the total score of the allied team in this round.

            :return:    The score as int.

                note::  Author(s): Mitch """

        score = 0
        for resultId in self.getResultIds():
            playerRound = BfPlayerRounds[int(resultId)]
            if playerRound.getTeamAtEnd() == 2:
                score += playerRound.getScore()

        return score

    def getScoreAxis(self):
        """ Function that calculates the total score of the axis team in this round.

            :return:    The score as int.

                note::  Author(s): Mitch """

        score = 0
        for resultId in self.getResultIds():
            playerRound = BfPlayerRounds[int(resultId)]
            if playerRound.getTeamAtEnd() == 1:
                score += playerRound.getScore()

        return score

    def getNumberOfNegativeScoresAllies(self):
        """ Function that counts the number of livePlayers with a negative score in the allied team.

            :return:    Number of livePlayers with negative scores.

                note::  Author(s): Mitch """

        n = 0
        for resultId in self.getResultIds():
            playerRound = BfPlayerRounds[int(resultId)]
            if playerRound.getTeamAtEnd() == 2 and playerRound.getScore() < 0:
                n += 1

        return n

    def getNumberOfNegativeScoresAxis(self):
        """ Function that counts the number of livePlayers with a negative score in the axis team.

                    :return:    Number of livePlayers with negative scores.

                        note::  Author(s): Mitch """

        n = 0
        for resultId in self.getResultIds():
            playerRound = BfPlayerRounds[int(resultId)]
            if playerRound.getTeamAtEnd() == 1 and playerRound.getScore() < 0:
                n += 1

        return n

    def countAxis(self):
        """ Function that counts the number of livePlayers in the axis team.

                    :return:    Number of livePlayers.

                        note::  Author(s): Mitch """

        count = 0
        for resultId in self.getResultIds():
            playerRound = BfPlayerRounds[int(resultId)]
            if playerRound.getTeamAtEnd() == 1:
                count += 1

        return count

    def countAllies(self):
        """ Function that counts the number of livePlayers in the allied team.

                    :return:    Number of livePlayers.

                        note::  Author(s): Mitch """

        count = 0
        for resultId in self.getResultIds():
            playerRound = BfPlayerRounds[int(resultId)]
            if playerRound.getTeamAtEnd() == 2:
                count += 1

        return count


LeagueRounds = LeagueRound.storageDict
