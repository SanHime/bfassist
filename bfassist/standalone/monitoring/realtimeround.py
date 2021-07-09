#############################################################################
#
#
# Module of BFA that manages server statistics in realtime
#
#
#############################################################################
""" This module implements the real-time logging of in-game statistics specifically for one current bf round.

    Dependencies:

        2nd-party dependency numpy

        bfassist <- (standalone.monitoring.)realtimeround
            |
            \-> bfa_logging
             -> standalone -> monitoring

        note::  Author(s): Mitch last-check: 08.07.2021 """

from datetime import datetime

from numpy import array, array2string

from bfassist.bfa_logging import log
from bfassist.standalone import Server
from bfassist.standalone.monitoring import RealTimePlayer, RealTimeVehicle, BfRound, BfServerSetting, BfPlayerRound, \
                                           Player


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class RealTimeRound:
    """ A real time round is supposed to correspond to a bf round in dice::xmlns::bf and contains all relevant
    information being updated in realtime. BfRounds in online mode are actually instantiated from the bfxml module that
     is parsing the bf round information.

        :param server:              The Server the real time round takes place.
        :param eventDict:           Dictionary containing all events with their timestamp as key.
        :param livePlayers:         Dictionary of real time live players with their ids as keys.
        :param dcedPlayers:         Dictionary of real time players that left during a running round.
                                    Now using their keyhash as key.
        :param liveTicketsAxis:     Current ticket count of axis.
        :param liveTicketsAllies:   Current ticket count of allies.
        :param roundStats:          Roundstats object from serverstats module.
        :param roundStart:          The start of the round as datetime.
        :param liveRound:           Flag that determines if a round is live and should be sent to the master when
                                    finished.

            todo::  Disconnecting/Reconnecting players could be handled together with a henk-patch?...
            note::  Author(s): Mitch """

    def __init__(self, server: Server, eventDict: dict = None, livePlayers: dict = None, dcedPlayers: dict = None,
                 liveTicketsAxis: int = None, liveTicketsAllies: int = None, roundStats: BfRound = None,
                 roundStart: datetime = None, liveRound: bool = False):

        self.server = server

        if eventDict:
            self.eventDict = eventDict
        else:
            self.eventDict = {}

        if livePlayers:
            self.livePlayers = livePlayers
        else:
            self.livePlayers = {}

        if dcedPlayers:
            self.dcedPlayers = dcedPlayers
        else:
            self.dcedPlayers = {}

        self.liveTicketsAxis = liveTicketsAxis
        self.liveTicketsAllies = liveTicketsAllies

        if roundStats:
            self.roundStats = roundStats
        else:
            self.roundStats = BfRound(self.server, BfServerSetting(), {}, datetime.now())

        if roundStart:
            self.roundStart = roundStart
        else:
            self.roundStart = self.roundStats.getStart()

        self.liveRound = liveRound

    # noinspection PyUnusedLocal
    def beginMedPack(self, player_id: int, player_location: array, medpack_status: int, healed_player: int):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateMedPackStatus(medpack_status)

    # noinspection PyUnusedLocal
    def beginRepair(self, player_id: int, player_location: array, repair_status: int, vehicle_type: str):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateRepairStatus(repair_status)

    # noinspection PyUnusedLocal
    def changePlayerName(self, player_id: int, player_location: array, name: str):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateName(name)

    # noinspection PyUnusedLocal
    def chat(self, player_id: int, player_location: array, team: int, text: str):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateTeam(team)

    def createPlayer(self, player_id: int, player_location: array, name: str, is_ai: int, team: int):
        new_player = RealTimePlayer(player_id, name, self.roundStats.getRoundId(), position=player_location,
                                    is_ai=is_ai, team=team)
        self.livePlayers[player_id] = new_player
        return new_player

    def destroyPlayer(self, player_id: int, player_location: array):
        player = self.livePlayers[player_id]
        player.updatePosition(player_location)
        self.livePlayers.pop(player_id)
        self.dcedPlayers[player.player.getKeyhash()] = player

    # noinspection PyUnusedLocal
    def destroyVehicle(self, player_id: int, player_location: array, vehicle: str, vehicle_pos: array):
        self.livePlayers[player_id].updatePosition(player_location)

    def disconnectPlayer(self, player_id: int, player_location: array):
        self.livePlayers[player_id].updatePosition(player_location)

    def endMedPack(self, player_id: int, player_location: array, medpack_status: int):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateMedPackStatus(medpack_status)

    def endRepair(self, player_id: int, player_location: array, repair_status: int):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateRepairStatus(repair_status)

    # noinspection PyUnusedLocal
    def enterVehicle(self, player_id: int, player_location: array, vehicle_name: str, player_seat: str, is_default: int,
                     is_fake: int):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateVehicle(RealTimeVehicle(position=player_location, is_fake=is_fake,
                                                                  seats={player_id: self.livePlayers[player_id]}))

    # noinspection PyUnusedLocal
    def exitVehicle(self, player_id: int, player_location: array, vehicle_name: str, is_fake: int):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateVehicle(None)

    def pickupFlag(self, player_id: int, player_location: array):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].pickupFlag()

    def pickupKit(self, player_id: int, player_location: array, kit):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].pickupKit(kit)

    # noinspection PyUnusedLocal
    def playerKeyHash(self, player_id: int, player_keyhash: str):
        self.livePlayers[player_id].player = self.server.playerLinks[player_id]

    # noinspection PyUnusedLocal
    def radioMessage(self, player_id: int, player_location: array, message: int, broadcast: int):
        self.livePlayers[player_id].updatePosition(player_location)

    def reSpawnEvent(self, player_id: int, player_location: array):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].spawn()

    def restartMap(self, tickets_team1: int, tickets_team2: int):
        self.liveTicketsAxis = tickets_team1
        self.liveTicketsAllies = tickets_team2

    def roundInit(self, tickets_team1: int, tickets_team2: int):
        self.liveTicketsAxis = tickets_team1
        self.liveTicketsAllies = tickets_team2

    def scoreEvent(self, player_id: int, player_location: array, score_type: str, victim_id: int, weapon: str):
        self.livePlayers[player_id].updatePosition(player_location)
        if score_type in ['Attack', 'Defence', 'FlagCapture', 'Objective', 'ObjectiveTK', 'Spawned', '(unknown)']:
            self.livePlayers[player_id].evaluate(score_type)
        elif score_type in ['Death', 'DeathNoMsg']:
            self.livePlayers[player_id].die()
        elif score_type == 'Kill':
            self.livePlayers[player_id].kill(victim_id, weapon)
        elif score_type == 'TK':
            self.livePlayers[player_id].teamKill(victim_id, weapon)

    def setTeam(self, player_id: int, player_location: array, team: int):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].updateTeam(team)

    def spawnEvent(self, player_id: int, player_location: array):
        self.livePlayers[player_id].updatePosition(player_location)
        self.livePlayers[player_id].spawn()

    @staticmethod
    def typeHintDcedPlayer():
        return {
            '__type__': dict,
            '__keys__': str,
            '__values__': RealTimePlayer.typeHint()
        }

    @classmethod
    def typeHint(cls):
        return {
                'dcedPlayers': cls.typeHintDcedPlayer(),
                'liveTicketsAxis': int,
                'liveTicketsAllies': int,
                'roundStart': str
            }

    def toLocalDict(self):
        """ Function for getting the real time round object as a dictionary of strings representing attributes and the
        values for the local bfa perspective so it can also be json serialised. (excluding event dict)

            :return:    Real time round as a dictionary.

                note::  Author(s): Mitch """

        return {
            'dcedPlayers':          {player_keyhash: self.dcedPlayers[player_keyhash].toLocalDict()
                                     for player_keyhash in self.dcedPlayers},
            'liveTicketsAxis':      self.liveTicketsAxis,
            'liveTicketsAllies':    self.liveTicketsAllies,
            'roundStart':           str(self.roundStart)
        }
