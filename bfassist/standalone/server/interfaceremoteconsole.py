#############################################################################
#
#
# Module of BFA introducing and managing the Remote Console Interface Class
#
#
#############################################################################
""" This module manages the interface and interactions of the server objects with their remote console.

    Dependencies:

        server <- interfaceremoteconsole
            |
            \-> bfcutil
             -> bfa_logging

        note::  Author(s): Mitch last-check: 08.07.2021 """

from random import randint
from threading import Lock

from bfassist.standalone.server import Server, RemoteConsole
from bfassist.standalone.server.bfcutil import buildHenkCommand
from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerRemoteConsoleInterface:
    """ The server remote console interface lets a server object interact with its remote console.

        :param server:              The server this interface belongs to.
        :param remoteConsole:       The remote console of this server for better readability.
        :param consoleLock:         The lock object that should prevent current access to the console.
        :param hasHenkPatch:        A dictionary containing 'names' of henk patches and a boolean value to indicate if
                                    they area accessible.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, remoteConsole: RemoteConsole = None, consoleLock: Lock = None,
                 hasHenkPatch: dict = None):
        self.server = server

        if remoteConsole:
            self.remoteConsole = remoteConsole
        else:
            self.remoteConsole = self.server.remoteConsole

        if consoleLock:
            self.consoleLock = consoleLock
        else:
            self.consoleLock = Lock()

        if hasHenkPatch:
            self.hasHenkPatch = hasHenkPatch
        else:
            self.hasHenkPatch = {
                'teleportation': False,
                'listPlayersMod': False,
                'changeTeam': False
            }

    def executeConsoleCommand(self, command: str, max_retries: int = 3):
        """ Function to execute a command on the Remote Console.

            :param command:     Command readable by Refractor Engine to be executed.
            :param max_retries: Maximum number of retries

            :return:            Response of Remote Console if there was any, otherwise None. False if execution failed.

                note::  Author(s): Mitch, uly """

        log("Executing a console command on a server.", 1)

        if not self.server.consoleIsAvailable:
            log('Tried to execute commands on a server without console availability.', 3)
            return None
        else:
            try:
                self.consoleLock.acquire(timeout=randint(1, 10))
                consoleResponse = self.remoteConsole.sendToConsole(command)
                log("Executed Task.", 1)
                return consoleResponse

            except TimeoutError:
                if max_retries == 0:
                    log('Retried to execute the same command: ' + command + ". The maximum amount of times. But " +
                        "console is still locked: " + str(self.consoleLock.locked()) +
                        " Aborting any further attempts.", 3)
                    return False
                else:
                    return self.executeConsoleCommand(command, max_retries-1)
            finally:
                self.consoleLock.release()

    def writeToServer(self, inMessage: str):
        """ Writes a BFA-Client server announcement to the server. Wraps lines with the word breaking the 64 char limit
        to avoid tearing words apart.

            :param inMessage:   Message to be announced to the server.

            :return:            True when done.

                note::  Author(s): Mitch """

        log("Writing a message to a server.", 0)
        inMessage += ' '
        currentMessagePart, inMessage = (inMessage[:inMessage.rfind(' ', 0, 63 - len('[BFA-Client]: '))],
                                         inMessage[inMessage.rfind(' ', 0, 63 - len('[BFA-Client]: ')):])
        while inMessage != ' ':
            self.executeConsoleCommand('game.sayAll \"[BFA-Client]: ' + currentMessagePart + "\"")
            currentMessagePart, inMessage = (inMessage[:inMessage.rfind(' ', 0, 63 - len('[BFA-Client]: '))],
                                             inMessage[inMessage.rfind(' ', 0, 63 - len('[BFA-Client]: ')):])
        self.executeConsoleCommand('game.sayAll \"[BFA-Client]: ' + currentMessagePart + "\"")

        return True

    def getPlayerList(self):
        """ Function that calls the listPlayers method and parses the output to a python list containing a set of player
        information of the list as a tuple.

            :return:    A list of tuples where each tuple represents one player dataset.

                note::  Author(s): Mitch """

        rawPlayerList = self.executeConsoleCommand('game.listPlayers')

        if rawPlayerList is None:
            log("Obtaining player-list from server failed.", 3)
            return None

        playerList = rawPlayerList.splitlines()
        finalPlayerList = set()

        # Parsing process should perhaps be further documented at some point

        # each entry of playerList should correspond to exactly one line of player information
        for playerInfo in playerList:

            # this is our base prerequisite to accept a line as a player
            if " is remote " in playerInfo:
                refined = playerInfo.split(' is remote ')

                # if a player name contained ' is remote ' we have to put this back inside their name
                while len(refined) > 2:
                    refined[0] += ' is remote ' + refined.pop(1)

                playerId = int(refined[0][3:refined[0].find(' ')])
                playerName = refined[0][refined[0].find(' ')+3:]

                # if the player is not a bot we also add keyhash and ip
                if ' is an AI bot.' not in refined[1]:
                    playerKeyhash = refined[1][refined[1].find('hash:')+5:]
                    playerIp = refined[1][refined[1].find('ip:')+4:refined[1].find('hash:')]
                # if the player is a bot we add that information instead
                else:
                    playerKeyhash = refined[0][refined[0].find(' ')+3:]
                    playerIp = ' is an AI bot.'
                # add a tuple containing the extracted information to the output list
                finalPlayerList.add((playerId, playerName, playerKeyhash, playerIp))
            else:
                if playerInfo.strip():
                    log("There was a none remote player? Player info: " + playerInfo)

        log("Finished parsing the console-output player-list.", 0)

        return finalPlayerList

    def teleportPlayerToPosition(self, player_id: str, position: str):
        """ Teleports a player via id to the specified position on the map.

            :param player_id:   Id of the player to teleport.
            :param position:    Position to teleport the player to.

                note::  Author(s): Mitch """

        if self.hasHenkPatch['teleportation']:
            self.executeConsoleCommand(buildHenkCommand(commandType='tpTo', args=[player_id, position]))

    def changeTeamOfPlayer(self, player_id: str):
        """ Changes the team of a player.

            :param  player_id:  Id of the player to change teams.

                note::  Author(s): Mitch, henk """

        if self.hasHenkPatch['changeTeam']:
            team = None
            self.execConsoleCommand(buildHenkCommand(commandType='setPlayerToTeam', args=[player_id, team]))

    def enableBots(self):
        """ Simple function to enable bots on the server.

                note::  Author(s): Mitch """

        self.writeToServer("Enabling bots on the server.")
        self.executeConsoleCommand("aiSettings.setRespawnAllowed 1")

    def disableBots(self):
        """ Simple function to disable bots on the server.

                note::  Author(s): Mitch """

        self.executeConsoleCommand("aiSettings.setRespawnAllowed 0")
        self.executeConsoleCommand("ai.killAllBots")

    def changeMapTo(self, mapName: str):
        """ Simple function to change to a different map.

            :param mapName:   Name of the map.

                ::important::   Probably can only switch to conquest mode maps and no mods as of now?!
                note::  Author(s): Mitch """

        self.writeToServer("Trying to change map to " + mapName + ".")
        self.executeConsoleCommand("admin.changeMap " + mapName + " conquest bf1942")

    def killPlayer(self, player_id: str):
        """ Simple function to kill a player based on its id.

            :param player_id:   Id of the player to kill.

                note::  Author(s): Mitch """

        self.writeToServer("Killing " + self.server.PlayerInterface.onlinePlayerWithId[player_id].name + ".")
        self.executeConsoleCommand("game.killPlayer " + player_id)

    def kickPlayer(self, player_id: str):
        """ Simple function to kick a player based on its id.

            :param player_id:   Id of the player to kick.

                note::  Author(s): Mitch """

        self.writeToServer("Kicking " + self.server.PlayerInterface.onlinePlayerWithId[player_id].name + ".")
        self.executeConsoleCommand("game.kickPlayer " + player_id)

    def banPlayer(self, player_id: str):
        """ Simple function to ban a player based on its id.

            :param player_id:   Id of the player to ban.

                note::  Author(s): Mitch """

        self.writeToServer("Banning " + self.server.PlayerInterface.onlinePlayerWithId[player_id].name + ".")
        self.executeConsoleCommand("admin.banPlayer " + player_id)

    def clearBanList(self):
        """ Simple function to clear the ban list of this server.

                note::  Author(s): Mitch, henk """

        self.executeConsoleCommand("admin.clearBanList")

    def getTimeLimit(self):
        """ Simple function to get the currently set time limit per round.

            :return:    Time limit in minutes as integer.

                note::  Author(s): Mitch """

        return int(self.executeConsoleCommand('game.timeLimit')[:-1])

    def setGameTime(self, gameTime: int):
        """ Simple function to set the currently set game time which corresponds to the time limit setting at boot time
        of the server.

            :gameTime:  Time limit in minutes as integer.

                note::  Author(s): Mitch """

        self.executeConsoleCommand('game.serverGameTime ' + str(gameTime))

    def postKeyhashOfPlayer(self, player_id: str):
        """ Posts the keyhash of a player to the public chat.

            :param player_id:   Id of the player that we will post the keyhash of.

                note::  Author(s): Mitch, henk """

        self.writeToServer(self.server.PlayerInterface.onlinePlayerWithId[player_id].player.getKeyhash())

    def postPositionOfPlayer(self, player_id: str):
        """ Posts the last known position of a player to the public chat.

            :param player_id:   Id of the player that we will post the keyhash of.

                note::  Author(s): Mitch, henk """

        self.writeToServer(self.server.PlayerInterface.onlinePlayerWithId[player_id].position)
