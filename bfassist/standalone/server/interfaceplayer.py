#############################################################################
#
#
# Module of BFA introducing and managing the Server Player Interface Class
#
#
#############################################################################
""" This module manages the interface and interactions of the bfa server objects with players on the server.

    Dependencies:

        standalone <- server <- interfaceplayer
            \
             -> monitoring

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.server import Server
from bfassist.standalone.monitoring import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerPlayerInterface:
    """ The Server Player Interface lets a server object interact with its players.

        :param server:              The server this interface belongs to.
        :param onlinePlayers:       A set of the players currently on the server, represented by their RealTimePlayer
                                    object.
        :param onlinePlayerWithId:  A dictionary containing the online players mapped to their ids for easier access.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, onlinePlayers: set = None, onlinePlayerWithId: dict = None):
        self.server = server
        if onlinePlayers:
            self.onlinePlayers = onlinePlayers
        else:
            self.onlinePlayers = set()

        if onlinePlayerWithId:
            self.onlinePlayerWithId = onlinePlayerWithId
        else:
            self.onlinePlayerWithId = {}

    @staticmethod
    def typeHintOnlinePlayers():
        return {
            '__type__': set,
            '__values__': RealTimePlayer.typeHint(),
        }

    def addPlayer(self, realTimePlayer: RealTimePlayer):
        """ Simple function that adds a real time player to the online players.

            :param realTimePlayer:  The real time player to add.

                note::  Author(s): Mitch """

        self.onlinePlayers.add(realTimePlayer)
        self.onlinePlayerWithId[playerId] = realTimePlayer

    def removePlayer(self, realTimePlayer: RealTimePlayer):
        """ Simple function to remove a real time player from the online players.

            :param realTimePlayer:  The real time player to remove.

                note::  Author(s): Mitch """

        self.onlinePlayerWithId.pop(realTimePlayer.Id)
        self.onlinePlayers.remove(realTimePlayer)

    def updateOnlinePlayers(self, playerList: set):
        """ Function that takes a set of tuples each containing a dataset that represents id, name, keyhash and ip
        of a player and uses it to update the online players.

            :param playerList:  A set of tuples containing current player information.

            note::  Author(s): Mitch """

        for playerInfo in playerList:
            playerId, playerName, playerKeyhash, playerIp = playerInfo

            if playerKeyhash not in Players:
                onlinePlayer = Player(playerKeyhash, playerName, {playerName}, Ips={playerIp})
            else:
                onlinePlayer = Players[playerKeyhash]
                onlinePlayer.addAlias(playerName)
                onlinePlayer.addIp(playerIp)

            if playerId not in self.onlinePlayerWithId:
                self.addPlayer(RealTimePlayer(playerId, playerName,
                                              self.server.StatsInterface.realTimeRound.roundStats.getRoundId(),
                                              onlinePlayer))

            else:
                realTimePlayer = self.onlinePlayerWithId[playerId]
                realTimePlayer.Name = playerName
                realTimePlayer.player = onlinePlayer

    def banPlayerByKeyhash(self, keyhash: str):
        """ Function that bans a player based on his keyhash. (Should be called from the ban module)

            :param keyhash: Keyhash of the player to ban.

                note::  Author(s): Mitch """

        player_id = self.playerIdFromKeyhash(keyhash)
        if player_id:
            self.banPlayer(player_id)
        self.server.ConsoleInterface.executeConsoleCommand("admin.addKeyToBanList " + keyhash)
        self.server.ConsoleInterface.writeToServer("Added a keyhash to the ban list.")

    def playerIdFromKeyhash(self, keyhash: str):
        """ Function that finds a player's id based on its keyhash if it's present on the server.

            :param keyhash:     Keyhash of the player.

            :return:            Id of the corresponding player. None if none such player could be found on the server.

                note::  Author(s): Mitch """

        for player_id in self.onlinePlayerWithId:
            if self.onlinePlayerWithId[player_id].player.getKeyhash() == keyhash:
                return player_id
        return None
