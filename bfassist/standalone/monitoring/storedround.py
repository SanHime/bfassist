#############################################################################
#
#
# Module of BFA that manages server round statistics
#
#
#############################################################################
""" This module implements the logging of Bf-Round Statistics.

    Dependencies:

        bfassist <- standalone <- monitoring <- storedround
            |
            \-> sql
             -> standalone  @BfRound.sendToMaster

        note::  Author(s): Mitch last-check: 08.07.2021 """

from __future__ import annotations

from datetime import datetime

from bfassist.standalone.monitoring import BfServerSetting, Player
from bfassist.standalone import Server
from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BfRound(DBStorable, table="serverstats", live=False):
    """ A BfRound is supposed to correspond to a bf round in dice::xmlns::bf and contains all relevant information.
    BfRounds in online mode are actually instantiated from the bfxml module that is parsing the bf round
    information.

        :param server:          The server the bf round took place.
        :param settings:        The settings the round was played with.
        :param results:         Information of the round end results as dictionary with player IDs as keys and
                                a list of BfPlayerRounds as values.


        :param RoundId:         The identifier of this particular round.
        :param ServerId:        The identifier of the server in the servers table.
        :param ResultIds:       A set of BfPlayerRound identifiers.
        :param Start:           Datetime of the start of the round.
                                (If we missed the round start we will set this the datetime the event log was created)

        :param End:             Datetime of the end of the round.
                                (End will equal start while the round is still being played)

                                (Can be None(/sqlite3.NULL if the settings weren't read before round start.)
        :param SettingsId:      The id of the settings in the settings table.

        :param Winner:          The winner of the round according to what bf considers winner.
                                0 means draw, 1 means axis won and 2 allied did.
        :param VType:           The victory type achieved according to bf. Ranges from 0 to 4 I believe.
        :param TicketsAxis:     Axis tickets at the end of the round.
        :param TicketsAllies:   Allied tickets at the end of the round.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, settings: BfServerSetting, results: dict, Start: datetime, RoundId: int = None,

                 End: datetime = None, ResultIds: set = None, ServerId: int = None, SettingsId: int = None,

                 Winner: int = None, VType: int = None, TicketsAxis: int = None, TicketsAllies: int = None):

        self.server = server
        self.settings = settings
        self.results = results

        self.SRoundId = RoundId, INTEGER, PRIMARY_KEY

        self.SStart = Start, DATETIME

        if End is not None:
            self.SEnd = End, DATETIME
        else:
            self.SEnd = Start, DATETIME

        if ResultIds is not None or self.results is None:
            self.SResultIds = ResultIds, VARCHAR(255)
        else:
            self.SResultIds = set(self.results.keys()), VARCHAR(255)

        if ServerId is not None or self.server is None:
            self.SServerId = ServerId, INTEGER
        else:
            self.SServerId = self.server.getBFAName(), VARCHAR(32)

        if SettingsId is not None or self.settings is None:
            self.SSettingsId = SettingsId, INTEGER
        else:
            self.SSettingsId = self.settings.getSettingsId(), INTEGER

        self.SWinner = Winner, BIT
        self.SVType = VType, TINYINT
        self.STicketsAxis = TicketsAxis, SMALLINT
        self.STicketsAllies = TicketsAllies, SMALLINT

        self.insertToDB()

    def sendToMaster(self):
        """ This function sends all the saved information of this round to the master server.

                note::  Author(s): Mitch """

        from bfassist.standalone import KERN

        log("Sending a round to master.")
        KERN.BFA_NETWORK.sendLeagueRound(self)

    def toGlobalDict(self):
        """ Function to convert a round to a dictionary for the global bfa perspective and to make it json serializable.

            :return:    Bf round as dictionary.

                note::  Author(s): Mitch """

        return {
            'server':           self.server.toGlobalDict(),
            'settings':         self.settings.toGlobalDict(),
            'results':          {Id: [result.toGlobalDict for result in self.results[Id]] for Id in self.results},
            'Start':            str(self.getStart()),
            'End':              str(self.getEnd()),
            'Winner':           self.getWinner(),
            'VType':            self.getVType(),
            'TicketsAxis':      self.getTicketsAxis(),
            'TicketsAllies':    self.getTicketsAllies()
        }

    def playedThisRound(self, player: Player):
        """ Checks if the specified player participated in this round.

            :param player   The player to check.

            :return:        True if they participated otherwise False.

                note::  Author(s): Mitch """

        for player_id in self.results:
            for result in self.results[player_id]:
                if result.getKeyhash() == player.getKeyhash():
                    return True

        return False


BfRounds = BfRound.storageDict
