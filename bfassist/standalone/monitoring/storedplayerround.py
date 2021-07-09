#############################################################################
#
#
# Module of BFA that is in charge of storing player rounds
#
#
#############################################################################
""" This module implements the logging and storing of Bf-Player-Rounds.

    Dependencies:

        bfassist <- (standalone.monitoring.)storedplayerround
            \
             -> sql

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BfPlayerRound(DBStorable, table="roundstats", live=False):
    """ A BfPlayerRound is supposed to correspond to the stats of a particular player in a particular bf round in
    dice::xmlns::bf and contains all information.

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

    def __init__(self, RoundId: int, PlayerId: int, Keyhash: str, NameAtEnd: str = None, IsAi: int = None,
                 TeamAtEnd: int = None, Score: int = None, Kills: int = None, Deaths: int = None, TeamKills: int = None,
                 Captures: int = None, Attacks: int = None, Defences: int = None, Objectives: int = None,
                 ObjectiveTeamKills: int = None, PlayerRoundId: int = None):

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

    @staticmethod
    def typeHint():
        return {
            'PlayerId': int,
            'Keyhash': str,
            'NameAtEnd': str,
            'IsAi': int,
            'TeamAtEnd': int,
            'Score': int,
            'Kills': int,
            'Deaths': int,
            'TeamKills': int,
            'Captures': int,
            'Attacks': int,
            'Defences': int,
            'Objectives': int,
            'ObjectiveTeamKills': int
        }

    def toGlobalDict(self):
        """ Function for turning a player round to a dictionary for the global bfa perspective and json serializable.

            :return:    Player round as dictionary.

                note::  Author(s): Mitch """

        return {
            'PlayerId':             self.getPlayerId(),
            'Keyhash':              self.getKeyhash(),
            'NameAtEnd':            self.getNameAtEnd(),
            'IsAi':                 self.getIsAi(),
            'TeamAtEnd':            self.getTeamAtEnd(),
            'Score':                self.getScore(),
            'Kills':                self.getKills(),
            'Deaths':               self.getDeaths(),
            'TeamKills':            self.getTeamKills(),
            'Captures':             self.getCaptures(),
            'Attacks':              self.getAttacks(),
            'Defences':             self.getDefences(),
            'Objectives':           self.getObjectives(),
            'ObjectiveTeamKills':   self.getObjectiveTeamKills()
        }


BfPlayerRounds = BfPlayerRound.storageDict
