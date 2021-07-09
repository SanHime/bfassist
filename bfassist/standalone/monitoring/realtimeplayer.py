#############################################################################
#
#
# Module of BFA that manages server statistics in realtime
#
#
#############################################################################
""" This module implements the real-time logging of in-game statistics specifically for one current bf player.

    Dependencies:

        2nd-party dependency numpy

        monitoring <- realtimeplayer

        note::  Author(s): Mitch last-check: 08.07.2021 """

from numpy import array, array2string

from bfassist.standalone.monitoring import Player
from bfassist.standalone.monitoring import RealTimeVehicle, BfPlayerRound, BfPlayerRounds


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class RealTimePlayer:
    """ A player that's playing on a server will have a corresponding real time player object to track it.

        :param Id:              Player id of the player.
        :param name:            Name of the player.
        :param currentRoundId:  Id of the round this player is currently participating in.
        :param player:          The corresponding bfa player object.
        :param score:           Round stats of this player.
        :param position:        Position of the player as numpy array.
        :param is_ai:           1 if the player is a bot otherwise 0.
        :param team:            Team the player is on.
        :param rotation:        Rotation of the player as numpy array.
        :param kit:             Kit the player is using.
        :param medpack_status:  Last known status of the med pack if medic, None if unknown.
        :param repair_status:   Last known status of the wrench if engineer, None if unknown.
        :param vehicle:         If the player is currently in a vehicle it can be found here otherwise this is None.

        :param hasFlag:         Boolean flag that indicates if the player has the flag in CTF.
        :param isSpawned:       Boolean flag that indicates if the player is currently spawned.

            ::important::       Real time objects use int for some parameter values that are usually string e.g. Id.
            note::  Author(s): Mitch, henk """

    def __init__(self, Id: int, name: str, currentRoundId: int, player: Player = None, score: BfPlayerRound = None,
                 position: array = None, is_ai: int = None, team: int = None, rotation: array = None, kit: str = None,
                 medpack_status: int = None, repair_status: int = None, vehicle: RealTimeVehicle = None,
                 hasFlag: bool = False, isSpawned: bool = False):

        self.Id = Id
        self.name = name
        self.currentRoundId = currentRoundId
        if score:
            self.score = score
        else:
            self.score = BfPlayerRounds[self.currentRoundId]
        self.player = player
        self.position = position
        self.is_ai = is_ai
        self.team = team
        self.rotation = rotation
        self.kit = kit
        self.medpack_status = medpack_status
        self.repair_status = repair_status
        self.vehicle = vehicle

        self.hasFlag = hasFlag
        self.isSpawned = isSpawned

    @staticmethod
    def typeHint():
        return {
            'Id': int,
            'name': str,
            'score': BfPlayerRound.typeHint(),
            'player': Player.typeHint(),
            'is_ai': int,
            'team': int,
            'rotation': str,
            'kit': str,
            'medpack_status': int,
            'repair_status': int,
            'vehicle': RealTimeVehicle.typeHint(),
            'hasFlag': bool,
            'isSpawned': bool
        }

    def updateName(self, name: str):
        """ Updates the name of this player.

            :param name:    The name to set.

                note::  Author(s): Mitch """

        self.name = name

    def pickupKit(self, kit: str):
        """ Updates the kit of this player.

            :param kit: The kit to set.

                note::  Author(s): Mitch """

        self.kit = kit

    def pickupFlag(self):
        """ Updates the flag carrier status of this player.

                note::  Author(s): Mitch """

        self.hasFlag = True

    def updateMedPackStatus(self, medpack_status: int):
        """ Updates the med pack status of this player.

            :param medpack_status:  Med pack status to set.

                note::  Author(s): Mitch """

        self.medpack_status = medpack_status

    def updateRepairStatus(self, repair_status: int):
        """ Updates the repair status of this player.

            :param repair_status:  Med pack status to set.

                note::  Author(s): Mitch """

        self.repair_status = repair_status

    def updateTeam(self, team: int):
        """ Updates the team of this player.

            :param team:    The team to set.

                note::  Author(s): Mitch """

        self.team = team

    def updatePosition(self, inPosition: array):
        """ Updates the position of this player.

            :param inPosition:  The newest position of this player.

                note::  Author(s): Mitch """

        self.position = inPosition

    def updateVehicle(self, inVehicle: RealTimeVehicle):
        """ Updates the vehicle of this player.

            :param inVehicle:   The real time vehicle to be set or None if none is used.

                note::  Author(s): Mitch """

        self.vehicle = inVehicle

    def spawn(self):
        """ Processes the spawning of this player.

                note::  Author(s): Mitch """

        self.isSpawned = True

    def die(self):
        """ Processes the death of this player and updates its round stats accordingly.

                note::  Author(s): Mitch """

        self.score.setDeaths(self.score.getDeaths() + 1)
        self.isSpawned = False

    # noinspection PyUnusedLocal
    def kill(self, victim_id: int, weapon: str):
        """ Processes a kill of this player and updates its round stats accordingly.

            :param victim_id:   Id of the victim.
            :param weapon:      Weapon used.

                note::  Author(s): Mitch """

        self.score.setKills(self.score.getKills() + 1)
        self.score.setScore(self.score.getScore() + 1)

    # noinspection PyUnusedLocal
    def teamKill(self, victim_id: int, weapon: str):
        """ Processes a team kill of this player and updates its round stats accordingly.

            :param victim_id:   Id of the victim.
            :param weapon:      Weapon used.

                note::  Author(s): Mitch """

        self.score.setKills(self.score.getTeamKills() + 1)
        self.score.setScore(self.score.getScore() - 2)

    def evaluate(self, score_type: str):
        """ Processes a score type event that's not Death, DeathNoMsg, Kill or TK.

            :param score_type:  Type of score event in
                                'Attack', 'Defence', 'FlagCapture', 'Objective', 'ObjectiveTK', 'Spawned', '(unknown)'

                note::  Author(s): Mitch """

        if score_type == 'Attack':
            self.score.setScore(self.score.getScore() + 2)
        elif score_type == 'Defence':
            self.score.setScore(self.score.getScore() + 5)
        elif score_type == 'FlagCapture':
            self.score.setScore(self.score.getScore() + 10)
        elif score_type == 'Objective':
            self.score.setScore(self.score.getScore() + 5)
        elif score_type == 'ObjectiveTK':
            self.score.setScore(self.score.getScore() - 15)
        elif score_type == 'Spawned':
            pass
        elif score_type == '(unknown)':
            pass

    def toLocalDict(self):
        """ Function for getting the real time player object as a dictionary of strings representing attributes and the
        values for the local bfa perspective so it can also be json serialised.

            :return:    Real time player as a dictionary.

                note::  Author(s): Mitch """

        return {
            'Id':               self.Id,
            'name':             self.name,
            'score':            self.score.toGlobalDict(),
            'player':           self.player.toGlobalDict(),
            'position':         "".join(array2string(self.position, separator='/')[1:-1].split()),
            'is_ai':            self.is_ai,
            'team':             self.team,
            'rotation':         "".join(array2string(self.rotation, separator='/')[1:-1].split()),
            'kit':              self.kit,
            'medpack_status':   self.medpack_status,
            'repair_status':    self.repair_status,
            'vehicle':          self.vehicle.toLocalDict(),
            'hasFlag':          self.hasFlag,
            'isSpawned':        self.isSpawned
        }
