#############################################################################
#
#
#   Monitoring Module to BFA c7 Standalone
#
#
#############################################################################
""" This is the monitoring module of bfa.

    Dependencies:

        monitoring ---> statusmessenger
                    |-> player
                    |-> realtimevehicle
                    |-> storedplayerround
                    |-> realtimeplayer
                    |-> storedsettings
                    |-> storedround
                    |-> realtimeround
                    \-> realtimeevent
                     -> logreader

        note::  Author(s): last-check: 08.07.2021 """

from bfassist.standalone.monitoring.statusmessenger import StatusMessenger
from bfassist.standalone.monitoring.player import Player, Players
from bfassist.standalone.monitoring.realtimevehicle import RealTimeVehicle
from bfassist.standalone.monitoring.storedplayerround import BfPlayerRound, BfPlayerRounds
from bfassist.standalone.monitoring.realtimeplayer import RealTimePlayer
from bfassist.standalone.monitoring.storedsettings import BfServerSetting, BfServerSettings
from bfassist.standalone.monitoring.storedround import BfRound, BfRounds
from bfassist.standalone.monitoring.realtimeround import RealTimeRound
from bfassist.standalone.monitoring.realtimeevent import RealTimeEvent
from bfassist.standalone.monitoring.logreader import LogReader


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass
