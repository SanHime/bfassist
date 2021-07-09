#############################################################################
#
#
#   Core Module to BFA c7 Standalone
#
#
#############################################################################
""" This is the Core Module of the BFA standalone. It can be run like a script to start the webservice of bfa.
The webservice contains a web API that can be controlled via HTTPS requests following a REST-like structure. The
webservice also provides a web UI generated by webgen that can be accessed from a browser. However, keep in mind that
bfa generates self-signed certificates if not provided with a signed certificate through the network config so that you
might have to force your browser to accept the self-signed certificate when trying to access it.

If run as script the other functions here are only accessed indirectly from the API. However, if one chooses to import
the module instead you can find the structurally most important functions here.

    Dependencies:

        bfassist <- standalone
            |
            |-> sql
            |-> webgen
            |-> standalone -\-> server
            |                -> monitoring
            |-> network ----\-> updatethread
            \                -> client
             -> standalone ---> api         @BFAKern.__init__
                            \-> webservice  @BFAKern.__init__
                             -> webclient   @BFAKern.run

        note::  Author(s): last-check: 08.07.2021 """

from __future__ import annotations

from time import sleep
from sys import executable, argv
from os import execl

from bfassist.bfa_logging import log
from bfassist.sql import *
from bfassist.webgen import View

from bfassist.standalone.server import Server, Servers
from bfassist.standalone.monitoring import Player, Players, StatusMessenger, LogReader

from bfassist.network import CONFIG, BFA_Settings, toggleAutoUpdate, toggleAutoUpgrade
from bfassist.network.updatethread import UpdateThread
from bfassist.network.client import BFA_CLIENT


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BFAKern:
    """ Centerpiece of a bfa client instance. Holds control over all involved modules.

        :param WEB_SERVICE:                 The webservice providing the API and web UI.
        :param BFA_NETWORK:                 The network client.
        :param CONFIG:                      The config specified from the config.ini in network.
        :param GLOBAL_MONITORING:           Boolean flag that indicates if global monitoring is turned on or off.
        :param REGISTERED_SERVERS:          A dbdictionary containing the servers managed by this kern.
        :param AUTO_UPDATE_THREAD:          A thread that can automatically pull updates and if specified also upgrade
                                            bfa at runtime.

        :param API:                         The API which is connected with the KERN.

            note::  Author(s): Mitch """

    def __init__(self, WEB_SERVICE: WebService = None, BFA_NETWORK: BFA_CLIENT = BFA_CLIENT, config: dict = CONFIG,
                 GLOBAL_MONITORING: bool = False, REGISTERED_SERVERS: DBDict = None,
                 AUTO_UPDATE_THREAD: UpdateThread = None, API: bfaAPI = None):

        from bfassist.standalone.api import BFA_FunctionApiMixIn, bfaAPI
        from bfassist.standalone.webservice import BFA_WEBSERVICE

        if WEB_SERVICE:
            self.WEB_SERVICE = WEB_SERVICE
        else:
            self.WEB_SERVICE = BFA_WEBSERVICE

        self.BFA_NETWORK = BFA_NETWORK
        self.CONFIG = config
        self.GLOBAL_MONITORING = GLOBAL_MONITORING

        if REGISTERED_SERVERS:
            self.REGISTERED_SERVERS = REGISTERED_SERVERS
        else:
            self.REGISTERED_SERVERS = Servers

        if AUTO_UPDATE_THREAD:
            self.AUTO_UPDATE_THREAD = AUTO_UPDATE_THREAD
            if self.CONFIG[BFA_Settings]['auto-upgrade']:
                self.AUTO_UPDATE_THREAD.auto_upgrading = True
                self.AUTO_UPDATE_THREAD.start()
            elif self.CONFIG[BFA_Settings]['auto-update']:
                self.AUTO_UPDATE_THREAD.start()

        else:
            self.AUTO_UPDATE_THREAD = UpdateThread(getUpdate=self.BFA_NETWORK.getUpdate)

        if API:
            self.API = API
        else:
            self.API = bfaAPI(self)

    def run(self):
        """ Function that sets the kern running. Essentially it builds all views and then starts the web service.

                note::  Author(s): Mitch """

        if not self.WEB_SERVICE.running:
            from bfassist.standalone.webclient import TOP_LEVEL_NAVIGATION_VIEWS
            log("Commencing with startup.")
            log("Building Views.")
            for view in TOP_LEVEL_NAVIGATION_VIEWS:
                if isinstance(view, View):
                    view.build()
            log("Starting the web service.")
            self.WEB_SERVICE.run()
            log("Use the webclient for simple administration. You can reach it on the hostname specified in the config"
                " on port 444 via HTTPS.")
            log("The setup user is: hash: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa user: admin pass: password")
        else:
            log("Webservice is already running", 3)

    def start(self):
        """ Function that turns global monitoring on and immediately hooks all registered servers to the framework.

            :return:    True in the end. (For the API)

                note::  Author(s): Mitch """

        log("Turning on global monitoring.")
        self.GLOBAL_MONITORING = True

        log("Hooking all registered servers to the framework.")
        for SERVER in self.REGISTERED_SERVERS:
            SERVER.MonitoringInterface.connect()
        return True

    def stop(self):
        """ Function that stops global monitoring.

            :return:    True in the end. (For the API)

                note::  Author(s): Mitch """

        log("Received stop, shutting BFA monitoring down.")
        if self.GLOBAL_MONITORING:
            self.GLOBAL_MONITORING = False

        log("Shutting down BFA monitoring for individual servers.")
        for SERVER in self.REGISTERED_SERVERS:
            if SERVER.MonitoringInterface.local_monitoring:
                SERVER.MonitoringInterface.disconnect()

        return True

    @staticmethod
    def fullReset():
        """ Function that is supposed to restart bfa fully.

                note::  Author(s): Mitch """

        execl(executable, executable, *argv)

    def upgrade(self):
        """ Function to get an update utilising the network module and self-restart entirely.

                note::  Author(s): Mitch """

        self.AUTO_UPDATE_THREAD.upgrade()

    def toggleAutoUpdate(self):
        """ Function to toggle the auto-update setting. Changes the setting in the config and adjusts the auto update
        thread accordingly.

            :return:    The new boolean value of the auto-update setting.

                note::  Author(s): Mitch """

        newValue = toggleAutoUpdate()
        if newValue:
            if not self.AUTO_UPDATE_THREAD.active:
                self.AUTO_UPDATE_THREAD.start()
        else:
            if not self.CONFIG[BFA_Settings]['auto-upgrade']:
                self.AUTO_UPDATE_THREAD.stop()
        return newValue

    def toggleAutoUpgrade(self):
        """ Function to toggle the auto-upgrade setting. Changes the setting in the config and adjusts the auto-update
        thread accordingly.

            :return:    The new boolean value of the auto-upgrade setting.

                note::  Author(s): Mitch """

        newValue = toggleAutoUpgrade()
        if newValue:
            if self.AUTO_UPDATE_THREAD.active:
                self.AUTO_UPDATE_THREAD.auto_upgrading = newValue
            else:
                self.AUTO_UPDATE_THREAD.auto_upgrading = newValue
                self.AUTO_UPDATE_THREAD.start()
        else:
            self.AUTO_UPDATE_THREAD.auto_upgrading = newValue
        return newValue

    def writeToAllServers(self, inMessage: str):
        """ This function writes a message to all hooked servers.

            :param inMessage:   The message to write.

                note::  Author(s): Mitch """

        for SERVER in self.REGISTERED_SERVERS:
            if SERVER.MonitoringInterface.local_monitoring and self.GLOBAL_MONITORING:
                SERVER.writeToServer(inMessage)

    def getServerSignatures(self):
        """ This function returns a dictionary containing all servers in the framework with their name as key and global
        dictionary as value.

            :return:    The dictionary containing the server signatures.

                note::  Author(s): Mitch """

        return {SERVER.getBFAName(): SERVER.toGlobalDict() for SERVER in self.REGISTERED_SERVERS}


KERN = BFAKern()