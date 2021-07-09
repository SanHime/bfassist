#############################################################################
#
#
# Module of BFA introducing and managing Server Class
#
#
#############################################################################
""" This module manages all direct interactions with the BF Servers managed by bfa.

    Dependencies:

        bfassist <- standalone <- server -----> remoteconsole
            |           |                   |-> core
            |           |                   |-> interfacemonitoring     @Server.__init__
            |           |                   |-> interfacebfexecutable   @Server.__init__
            |           |                   |-> interfacemap            @Server.__init__
            |           |                   |-> interfaceremoteconsole  @Server.__init__
            |           |                   |-> interfaceplayer         @Server.__init__
            |           |                   \-> interfacestats          @Server.__init__
            |           |                    -> interfacesettings       @Server.__init__
            |           |-> admin
            |           \-> server -> interfaceplayer       @Server.typeHint
            |            -> monitoring -\-> realtimeround   @Server.typeHint
            |                            -> storedsettings  @Server.typeHint
            \-> standalone -> monitoring -> realtimeRound   @Server.toLocalDict
             -> standalone  @Server.monitoringIsActive


        note::  Author(s): Mitch last-check: 08.07.2021 """

from __future__ import annotations

from bfassist.standalone.server.remoteconsole import RemoteConsole
from bfassist.standalone.server.core import ServerCore


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Server(ServerCore):
    """ A Server represents the BF-A representation of a bf server. It contains useful functions such as the possibility
    to execute a command through the remote console. Write messages as server announcement. Online manipulation of
    server-files and deployment of files to be included via the refractor engine. And all other necessary functions for
    keeping relevant server information updated.

        :param BFAName:                 The name of this server within bfa.
        :param BFPath:                  The path to the executable of this server.
        :param MonitoringInterface:     The monitoring interface for this server.
        :param ExecutableInterface:     The executable interface for this server.
        :param MapInterface:            The map interface for this server.
        :param ConsoleInterface:        The console interface for this server.
        :param PlayerInterface:         The player interface for this server.
        :param StatsInterface:          The statistics interface for this server.
        :param SettingsInterface:       The settings interface for this server.
        :param InGameAdministration:    The classic in-game administration.

            note::  Author(s): Mitch """

    def __init__(self, BFAName: str, BFPath: str, MonitoringInterface: ServerMonitoringInterface = None,
                 ExecutableInterface: ServerExecutableInterface = None, MapInterface: ServerMapInterface = None,
                 ConsoleInterface: ServerRemoteConsoleInterface = None, PlayerInterface: ServerPlayerInterface = None,
                 StatsInterface: ServerStatisticsInterface = None, SettingsInterface: ServerSettingsInterface = None,
                 InGameAdministration: ServerAdministration = None):

        from bfassist.standalone.server.interfacemonitoring import ServerMonitoringInterface
        from bfassist.standalone.server.interfacebfexecutable import ServerExecutableInterface
        from bfassist.standalone.server.interfacemap import ServerMapInterface
        from bfassist.standalone.server.interfaceremoteconsole import ServerRemoteConsoleInterface
        from bfassist.standalone.server.interfaceplayer import ServerPlayerInterface
        from bfassist.standalone.server.interfacestats import ServerStatisticsInterface
        from bfassist.standalone.server.interfacesettings import ServerSettingsInterface
        from bfassist.standalone.admin import ServerAdministration

        super().__init__(BFAName, BFPath)

        if MonitoringInterface:
            self.MonitoringInterface = MonitoringInterface
        else:
            self.MonitoringInterface = ServerMonitoringInterface(self)

        if ExecutableInterface:
            self.ExecutableInterface = ExecutableInterface
        else:
            self.ExecutableInterface = ServerExecutableInterface(self)

        if MapInterface:
            self.MapInterface = MapInterface
        else:
            self.MapInterface = ServerMapInterface(self)

        self.MapInterface.refreshMaps()  # remove line with comment for disabling refreshing maps

        if ConsoleInterface:
            self.ConsoleInterface = ConsoleInterface
        else:
            self.ConsoleInterface = ServerRemoteConsoleInterface(self)

        if PlayerInterface:
            self.PlayerInterface = PlayerInterface
        else:
            self.PlayerInterface = ServerPlayerInterface(self)

        if StatsInterface:
            self.StatsInterface = StatsInterface
        else:
            self.StatsInterface = ServerStatisticsInterface(self)

        if SettingsInterface:
            self.SettingsInterface = SettingsInterface
        else:
            self.SettingsInterface = ServerSettingsInterface(self)

        if InGameAdministration:
            self.InGameAdministration = InGameAdministration
        else:
            self.InGameAdministration = ServerAdministration(self)

    def __setattr__(self, key: str, value, getOriginal: bool = False):
        if key[1:] in super().column_definitions:
            super().__setattr__(key, value)
        else:
            super().__setattr__(key, value, True)

    def __repr__(self):
        """ Sets string representation of a Server Object.

                note::  Author(s): Mitch """

        return str(self.toLocalDict())

    def __str__(self):
        """ Sets casting to string of a Server Object.

                note::  Author(s): Mitch """

        return str(self.toLocalDict())

    @staticmethod
    def typeHint():
        from bfassist.standalone.server.interfaceplayer import ServerPlayerInterface
        from bfassist.standalone.monitoring.realtimeround import RealTimeRound
        from bfassist.standalone.monitoring.storedsettings import BfServerSetting
        return {
            'BFAName': str,
            'BFPath': str,
            'consoleUsername': str,
            'consolePassword': str,
            'ip': str,
            'consolePort': str,
            'gamePort': str,
            'consoleIsAvailable': bool,
            'local_monitoring': bool,
            'creationTimeLastLog': str,
            'greeting': bool,
            'onlinePlayers': ServerPlayerInterface.typeHintOnlinePlayers(),
            'settings': BfServerSetting.typeHint(),
            'realTimeRound': RealTimeRound.typeHint()
        }

    def toLocalDict(self):
        """ Function for getting the server object as a dictionary of strings representing attributes and their values
        for the local bfa perspective so it can also be json serialised.

            :return:    Server as a dictionary.

                note::  Author(s): Mitch """

        from bfassist.standalone.monitoring.realtimeround import RealTimeRound

        if self.StatsInterface.realTimeRound is None:
            self.StatsInterface.realTimeRound = RealTimeRound(self)

        return {
            'BFAName':              self.getBFAName(),
            'BFPath':               self.getBFPath(),
            'consoleUsername':      self.consoleUsername,
            'consolePassword':      self.consolePassword,
            'ip':                   self.ip,
            'consolePort':          self.consolePort,
            'gamePort':             self.gamePort,
            'consoleIsAvailable':   self.consoleIsAvailable,
            'local_monitoring':     self.MonitoringInterface.local_monitoring,
            'creationTimeLastLog':  str(self.MonitoringInterface.creationTimeLastLog),
            'greeting':             self.MonitoringInterface.greeting,
            'onlinePlayers':        {player.Id: player.toLocalDict() for player in self.PlayerInterface.onlinePlayers},
            'settings':
                self.SettingsInterface.settings.toGlobalDict() if self.SettingsInterface.settings
                else None,
            'realTimeRound':        self.StatsInterface.realTimeRound.toLocalDict(),
        }

    def toGlobalDict(self):
        """ Simple function for getting the server object as a dictionary for the global bfa perspective so it can also
         be json serialised.

            :return:    Server as a dictionary.

                note::  Author(s): Mitch """

        return {
            'BFAName':                  self.getBFAName(),
            'dynamicExecutable':
                self.ExecutableInterface.dynamicExecutable.toGlobalDict() if self.ExecutableInterface.dynamicExecutable
                else 'unknown',
            'ip':                       self.ip,
            'gamePort':                 self.gamePort,
            'local_monitoring':         self.MonitoringInterface.local_monitoring,
            'hasHenkPatch':             self.ConsoleInterface.hasHenkPatch
        }

    def monitoringIsActive(self):
        """ Simple function to check if monitoring is still active globally and for this server.

            :return:    True if active, False otherwise.

                note::  Author(s): Mitch """

        from bfassist.standalone import KERN

        if self.MonitoringInterface.local_monitoring and KERN.GLOBAL_MONITORING:
            return True
        else:
            return False


Servers = Server.storageDict
