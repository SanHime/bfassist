#############################################################################
#
#
# Module of BFA introducing and managing the Server Monitoring Interface Class
#
#
#############################################################################
""" This module manages the interface and interactions of the bfa server objects with the bfa monitoring module.

    Dependencies:

        bfassist <- standalone <- server <- interfacemonitoring
            |
            \-> standalone  @ServerMonitoringInterface.connect
             -> bfa_logging

        note::  Author(s): Mitch last-check: 08.07.2021 """

from glob import glob
from datetime import datetime
from os import remove
from os.path import getmtime, getctime
from subprocess import Popen, PIPE, TimeoutExpired
from time import sleep

from bfassist.standalone.server import Server
from bfassist.standalone import StatusMessenger, LogReader
from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerMonitoringInterface:
    """ The Server Monitoring Interface lets a server object be monitored and partly controlled by the monitoring
    module.

        :param server:              The server this interface belongs to.
        :param local_monitoring:    A boolean flag that indicates if the server is being monitored locally.
        :param creationTimeLastLog: Datetime of the creation of the last event log.
        :param eventLogFeed:        Feed of the current event log.
        :param statusMessenger:     The status messenger of this server.
        :param logReader:           The log reader of this server.
        :param greeting:            A boolean flag that indicates if the server should greet players.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, local_monitoring: bool = False, creationTimeLastLog: datetime = None,
                 eventLogFeed: Popen = None, statusMessenger: StatusMessenger = None, logReader: LogReader = None,
                 greeting: bool = True):

        self.server = server
        self.local_monitoring = local_monitoring
        self.creationTimeLastLog = creationTimeLastLog
        self.eventLogFeed = eventLogFeed

        if statusMessenger:
            self.statusMessenger = statusMessenger
        else:
            self.statusMessenger = StatusMessenger(self.server)

        if logReader:
            self.logReader = logReader
        else:
            self.logReader = LogReader(self.server, self.eventLogFeed)

        self.greeting = greeting

    def connect(self):
        """ This function is supposed to hook the corresponding Bf1942 Server of a Server Object into the BFA monitoring
        framework.

            :return:            True if it succeeds putting the server up or it's already running, False otherwise.

                note::  Author(s): Mitch """

        from bfassist.standalone import KERN

        if not KERN.GLOBAL_MONITORING:
            log("Monitoring is globally turned off right now. Switching it on to start monitoring for this server.")
            KERN.GLOBAL_MONITORING = True

        log("Hooking a server to the framework.", 1)
        if not self.local_monitoring and self.server.fullTest():
            self.addEventLogFeed()
            self.local_monitoring = True
            log("Local monitoring started for a server, commencing with monitoring.", 1)
            self.startMonitoring()
            return True
        elif not self.local_monitoring:
            log("Couldn't start local monitoring for a server as the full test failed.", 3)
            return False
        else:
            log("Tried to start local monitoring for a server that was already being monitored.")
            return True

    def disconnect(self):
        """ Function that should be called when disconnecting the Server from the BFA-Framework. Importantly, shutting
        down the SSH-Sessions tailing the logs.

            :return:    True if successfully shut down. False if already offline.

                note::  Author(s): Mitch """

        if not self.local_monitoring:
            # server is already in offline mode
            return False
        log("Preparing to disconnect a server from the framework.")
        self.server.ConsoleInterface.writeToServer("Disconnecting from BFA!")
        self.server.remoteConsole.disconnect()
        self.stopMonitoring()
        log("Closing feeds.")
        try:
            self.eventLogFeed.terminate()
            self.eventLogFeed.communicate(timeout=5)
            self.eventLogFeed = None
        except TimeoutExpired:
            self.eventLogFeed = None

        log("Server successfully disconnected.")
        return True

    def cleanEventLogs(self):
        """ Deletes all event logs older than 1 month (30 days) to prevent overcrowding of event logs.

                note::  Author(s): Mitch """

        log("Cleaning event logs on a server.")
        logFileList = glob(self.server.getBFPath() + "mods/bf1942/logs/*.xml")
        for file in logFileList:
            if datetime.now().timestamp() - getmtime(file) > 60*60*24*30:
                remove(file)
        log("Cleaned event logs on a server.", 1)

    def addEventLogFeed(self):
        """ Starts tailing the newest event log and feeds it to the respective hook in the interface. Also calls clean
        event logs at the start.

                note::  Author(s): Mitch """

        self.cleanEventLogs()
        log("Adding feed from event log.", 1)
        logFileList = glob(self.server.getBFPath() + "mods/bf1942/logs/*.xml")
        latest_file = max(logFileList, key=getmtime)
        self.creationTimeLastLog = datetime.fromtimestamp(getctime(latest_file))
        bashCommand = 'tail -f -n 1 ' + str(latest_file)
        if self.eventLogFeed:
            try:
                self.eventLogFeed.terminate()
                self.eventLogFeed.communicate(timeout=5)
                self.eventLogFeed = None
            except TimeoutExpired:
                self.eventLogFeed = None
        self.eventLogFeed = Popen(bashCommand.split(), stdout=PIPE, stdin=PIPE, encoding="latin_1")
        self.logReader = LogReader(self.server, self.eventLogFeed)
        log("Added feed from event log.", 0)

    def renewEventFeed(self):
        """ Renews the feeding of the event log when it's reached the end of a log. Also cleans old logs on the fly.

                note::  Author(s): Mitch """

        log("Renewing event feed of a server.", 1)
        sleep(3)
        self.addEventLogFeed()
        log("Finished renewing event feed of a server.", 0)

    def bootPlayers(self):
        """ Function to update the active players using the remote console output of game.listPlayers.

                note::  Author(s): Mitch """

        log("Asking console for player-list on server.", 0)
        playerList = self.server.ConsoleInterface.getPlayerList()
        self.server.PlayerInterface.updateOnlinePlayers(playerList)

    def startMonitoring(self):
        """ Starts the monitoring threads for the specified server.

                note::  Author(s): Mitch """

        log("Starting monitoring for server.")
        if not self.statusMessenger.is_alive():
            self.statusMessenger = StatusMessenger(self.server)
        self.statusMessenger.start()
        sleep(.1)
        self.bootPlayers()
        sleep(.1)
        if not self.logReader.is_alive():
            self.logReader = LogReader(self.server, self.eventLogFeed)
        self.logReader.start()
        log("Started monitoring for server.", 1)

    def stopMonitoring(self):
        """ Stops the monitoring threads for the specified server.

                note::  Author(s): Mitch """

        if self.statusMessenger:
            self.local_monitoring = False
            log("Waiting for the status messenger to join.")
            self.statusMessenger.join(timeout=5)
        if self.logReader:
            self.local_monitoring = False
            log("Waiting for the log reader to join.")
            self.logReader.join(timeout=5)
