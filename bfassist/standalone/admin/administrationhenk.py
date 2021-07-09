#############################################################################
#
#
#   BFA Standalone Henk Administration Module to BFA c7
#
#
#############################################################################
""" This module provides some administration tools provided through henk-patches.

    Dependencies:

        2nd-party dependency numpy

        bfassist <- standalone <- (admin.)administrationhenk
            |
            \-> standalone -> admin
             -> usersystem


        note::  Author(s): Mitch last-check: 08.07.2021 """

from numpy import array

from bfassist.standalone import Server
from bfassist.standalone.admin import ServerAdministration
from bfassist.usersystem import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class HenkAdministration(ServerAdministration):
    """ Extension of the server administration that handles administrative tasks made possible by henk patches.

            note::  Author(s): Mitch """

    currentModulePrefix = '!'
    ServerAdministration.triggers.add(currentModulePrefix)
    ServerAdministration.inGameCommands[currentModulePrefix] = {}
    usageOf = []

    def __init__(self, server: Server):
        super().__init__(server)

    def teleport(self, player_id: int, player_position: array):
        """ This function teleports a player by his id to the issuing player on the server,
        all information should be passed to args.

            :param player_id:       Player id of the player to teleport.
            :param player_position: The position of the issuing player as x,y,z coordinates in numpy array .

                note::  Author(s) Mitch """

        log("Performing teleportation to a Player.", 1)
        self.server.ConsoleInterface.teleportPlayerToPosition(player_id, player_position)
    usageOf += [(teleport, 'tp', Admin)]

    def teleportTo(self, player_id: int, player_position: array):
        """ This function teleports a player by his id to coordinates, all information should be passed to args.

            :param player_id:       Player id of the player to teleport.
            :param player_position: The x,y,z coordinates as numpy array.

                note::  Author(s) Mitch """

        self.server.ConsoleInterface.teleportPlayerToPosition(player_id, player_position)
    usageOf += [(teleportTo, 'tpTo', Admin)]

    def changeTeamOfPlayer(self, player_id: int):
        """ This function changes the team of a player.

            :param player_id:   Player id of the player to change teams.

                note::  Author(s): henk, Mitch """

        self.server.ConsoleInterface.changeTeamOfPlayer(player_id)
    usageOf += [(changeTeamOfPlayer, 'changeTeam', Admin)]


ServerAdministration = HenkAdministration
ServerAdministration.updateUsages()
