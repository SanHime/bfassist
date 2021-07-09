#############################################################################
#
#
# Module of BFA introducing and managing Server Core Class
#
#
#############################################################################
""" This module manages all core and structural interactions with the BF Servers managed by bfa.

    Dependencies:

        bfassist <- (standalone.)server <- core
            |
            \-> sql
             -> bfa_logging

        note::  Author(s): Mitch last-check: 08.07.2021 """

from os import stat
from os.path import exists
from time import time

from bfassist.standalone.server import RemoteConsole
from bfassist.sql import *
from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerCore(DBStorable, table="bfaservers", live=False):
    """ A Server Core represents the most basic and abstract representation of a bf server that's managed by bfa.
    In particular the most important structural functions like the console and path tests can be found here.

        :param BFAName:             BFA name of this server.
        :param BFPath:              Path to the game folder of this server.

        :param consoleUsername:     The username for the remote console.
        :param consolePassword:     The password for the remote console.
        :param ip:                  The ip address that's filled in the server manager config to be used for the server.
        :param consolePort:         The port of the remote console.
        :param gamePort:            The game port of the bf server.
        :param consoleIsAvailable:  A boolean flag to indicate if the remote console is currently available.

        :param remoteConsole:       The remote console object that connects to the remote console of the bf server.

            note::  Author(s): Mitch """

    def __init__(self, BFAName: str, BFPath: str,

                 consoleUsername: str = None, consolePassword: str = None, ip: str = None, consolePort: str = None,
                 gamePort: str = None,

                 consoleIsAvailable: bool = False, remoteConsole: RemoteConsole = None, ):

        self.SBFAName = BFAName, VARCHAR(32), PRIMARY_KEY
        self.SBFPath = BFPath, VARCHAR(255)

        self.insertToDB()

        if consoleUsername:
            self.consoleUsername = consoleUsername
        if consolePassword:
            self.consolePassword = consolePassword
        if ip:
            self.ip = ip
        if consolePort:
            self.consolePort = consolePort
        if gamePort:
            self.gamePort = gamePort
        if remoteConsole:
            self.remoteConsole = remoteConsole

        self.consoleIsAvailable = consoleIsAvailable

        if BFPath is None:
            return
        else:
            consoleInfo = self.readServerManagerConfig()
            if consoleInfo:
                self.consoleUsername, self.consolePassword, self.ip, self.consolePort, self.gamePort = consoleInfo
            else:
                self.consoleUsername, self.consolePassword, self.ip, self.consolePort, self.gamePort = (None, )*5

            self.remoteConsole = RemoteConsole(self.consoleUsername, self.consolePassword, self.ip, self.consolePort)

    def __init_subclass__(cls, **kwargs):
        """ This is needed to allow inheritance of this class without calling the init_subclass method of DBStorable."""
        pass

    def readServerManagerConfig(self):
        """ Function that reads ip, game port, console port, console user and console password from the
        servermanager.con file of bfsm and returns them.

            :return:    A tuple of ip, game port, console port, console user and console password in this order.

                todo::  Not sure where this develops towards. Could parse entire config but there is a plan to exclude
                        bfsm in the future so it wouldn't really make much sense.
                note::  Author(s): Mitch """

        if exists(self.getBFPath() + 'mods/bf1942/settings/servermanager.con'):

            with open(self.getBFPath() + 'mods/bf1942/settings/servermanager.con') as bfsmConFile:
                bfsmConfig = bfsmConFile.readlines()
                for line in bfsmConfig:
                    if line.startswith('game.serverIP'):
                        ip = line[len('game.serverIP '):-1]
                    elif line.startswith('game.serverPort'):
                        gamePort = line[len('game.serverPort '):-1]
                    elif line.startswith('manager.consolePort'):
                        consolePort = line[len('manager.consolePort '):-1]
                    elif line.startswith('manager.consoleUsername'):
                        consoleUser = line[len('manager.consoleUsername ')+1:-2]
                    elif line.startswith('manager.consolePassword'):
                        consolePassword = line[len('manager.consolePassword ')+1:-2]
            log("Using ip=" + ip + " serverPort=" + gamePort + " consolePort=" + consolePort + " consoleUsername=" +
                consoleUser + " consolePassword=" + consolePassword)
            return consoleUser, consolePassword, ip, consolePort, gamePort
        else:

            log("Could not find servermanager.con at " + self.getBFPath() +
                'mods/bf1942/settings/servermanager.con. Server setup will be invalid!', 4)

    def addConsoleHandle(self):
        """ Function to make the remote console usage available for this server.

            :return: True if already authenticated or authentication-procedure succeeds. False otherwise.

                note::  Author(s): Mitch """

        if self.remoteConsole.authenticated:
            self.consoleIsAvailable = True
            log("Console handle added.", 0)
            return True
        else:
            self.remoteConsole.renewSocket()
            if self.remoteConsole.authenticate():
                self.consoleIsAvailable = True
                log("Console handle added.", 0)
                return True
            else:
                log("Couldn't add console handle!", 4)
                return False

    def pathTest(self):
        """ This function tests if all files required for hooking this server into the BFA Framework can be found at the
         location specified by the corresponding Server Object.

            :return:    True if the test was successful otherwise False.

                note::  Author(s): Mitch """

        # Checking for bfsmd.log
        if not exists(self.getBFPath() + "bfsmd.log"):
            log("bfsmd.log for " + self.getBFAName() + " could not be found at " + self.getBFPath(), 4)
            return False

        # Checking for existence of event logs
        if not exists(self.getBFPath() + "/mods/bf1942/logs/bflog_local.log"):
            log("Event logs for " + self.getBFAName() + " could not be found at " + self.getBFPath(), 4)
            return False

        # Making sure Event logs are up to date
        if stat(self.getBFPath() + "/mods/bf1942/logs/bflog_local.log").st_mtime < time() - 7 * 86400:
            log("Event log for " + self.getBFAName() +
                " isn't up to date. Is the server offline or event logging disabled?", 4)
            return False

        log("Successfully performed pathTest.", 1)
        return True

    def fullTest(self):
        """ This function tests if this Server Object is ready to be hooked into the BFA framework. Tested are
         availability of the RemoteConsole and the path to the game directory.

            :return:    True if the test was successful otherwise False.

                note::  Author(s): Mitch """

        if not self.consoleIsAvailable and not self.addConsoleHandle():
            log("RemoteConsole Failure when performing fullTest.", 4)
            return False
        elif not self.pathTest():
            log("Game Path Failure when performing fullTest.", 4)
            return False
        else:
            return True

    def editServer(self, newBFPath: str, newBFAName: str):
        """ Simple function to edit the server core.

            :param newBFPath:   The new path to the bf binary.
            :param newBFAName:  The new internal name of the server.

            :return:            True at the end of editing.

                note::  Author(s): Mitch """

        self.setBFPath(newBFPath)
        self.setBFAName(newBFAName)
        return True
