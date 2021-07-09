#############################################################################
#
#
#   BFA Standalone Basic Administration Module to BFA c7
#
#
#############################################################################
""" This module provides the base administrative functions for the administration of a bf server. That includes kicks,
bans, etc..

    Dependencies:

        bfassist <- standalone <- (admin.)administrationbasic
            |
            \-> standalone -> admin
             -> usersystem

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone import Server
from bfassist.standalone.admin import ServerAdministration
from bfassist.usersystem import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerAdministrationBasic(ServerAdministration):
    """ Basic extension of the server administration that handles warnings, kicks, etc..

        :param server:          The server this administration extension belongs to.
        :param modulePrefix:    The prefix that applies to the functions described in this module.

            note::  Author(s): Mitch """

    currentModulePrefix = '!'
    ServerAdministration.triggers.add(currentModulePrefix)
    ServerAdministration.inGameCommands[currentModulePrefix] = {}
    usageOf = []

    def __init__(self, server: Server):
        super().__init__(server)

    def ban(self, player_id: int, ban_reason: str = ""):
        """ This function bans a player utilising the ban system (atm just ban via keyhash!?).

            :param player_id:   Player id of the player to be banned and the reason for the ban.
            :param ban_reason:  Reason for the ban if any was specified.

                note::  Author(s): henk, Mitch """

        from bfassist.standalone.server.bans import Ban

        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            Ban(self.server, self.server.PlayerInterface.onlinePlayerWithId[player_id].player.getKeyhash(),
                Reason=ban_reason)
    usageOf += [(ban, 'ban', Admin)]

    def kick(self, player_id: int):
        """ This function simply kicks a player from the server.

            :param player_id:   Player id of the player to be kicked.

                note::  Author(s): henk, Mitch """

        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            self.server.ConsoleInterface.kickPlayer(player_id)
    usageOf += [(kick, 'kick', Admin)]

    def kill(self, player_id: int):
        """ This function simply kills a player on the server.

            :param player_id:   Player id of the player to be killed.

                note::  Author(s): henk, Mitch """

        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            self.server.ConsoleInterface.killPlayer(player_id)
    usageOf += [(kill, 'kill', Admin)]

    def changeMap(self, mapName: str):
        """ This function changes the map on the server. (Disabled until BFSM fully replaced)

            :param mapName: Name of the map to change to.

                note::  Author(s): henk, Mitch """

        # self.server.ConsoleInterface.changeMapTo(mapName)
        pass

    def warnDis(self, player_id: int):
        """ This function warns a player for disruptive game play.

            :param player_id:   Id of the player to warn.

                note::  Author(s): henk, Mitch """

        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            self.server.ConsoleInterface.writeToServer(self.server.PlayerInterface.onlinePlayerWithId[player_id] +
                                                       " please don't player disruptively.")
    usageOf += [(warnDis, 'wdis', Admin)]

    def warnTk(self, player_id: int):
        """ This function warns a player for team killing.

            :param player_id:   Id of the player to warn.

                note::  Author(s): henk, Mitch """

        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            self.server.ConsoleInterface.writeToServer(self.server.PlayerInterface.onlinePlayerWithId[player_id] +
                                                       " please don't team-kill.")
    usageOf += [(warnTk, 'wtk', Admin)]

    def paraInfo(self):
        """ This function posts information about a parachute spawn to the server.

                note::  Author(s): henk, Mitch """

        self.server.ConsoleInterface.writeToServer("Get a parachute spawn at the island by capturing a flag at sea.")
    usageOf += [(paraInfo, 'paraInfo', Default)]

    def removeBots(self):
        """ This function removes any bots from the server.

                note::  Author(s): henk, Mitch """

        self.server.ConsoleInterface.disableBots()
    usageOf += [(removeBots, 'noBots', Admin)]

    def addBots(self):
        """ This function tuns on bots on the server.

                note::  Author(s): henk, Mitch """

        self.server.ConsoleInterface.enableBots()
    usageOf += [(addBots, 'bots', Admin)]

    def nextmap(self):
        """ ... (Not sure what this is supposed to do)

                note::  Author(s): henk, Mitch """

        pass
    usageOf += [(nextmap, 'nextmap', Default)]

    def key(self, player_id: int):
        """ Function that prints the keyhash of the issuing player to the server chat.

            :param player_id:    Id of the issuing player.

                note::  Author(s): henk, Mitch """

        self.server.ConsoleInterface.postKeyhashOfPlayer(player_id)
    usageOf += [(key, 'key', Default)]

    def loc(self, player_id: int):
        """ Function that prints the position of the issuing player at issue.

            :param player_id:   Id of the issuing player.

                note::  Author(s): henk, Mitch """

        self.server.ConsoleInterface.postPositionOfPlayer(player_id)
    usageOf += [(loc, 'loc', Default)]


ServerAdministration = ServerAdministrationBasic
ServerAdministration.updateUsages()
