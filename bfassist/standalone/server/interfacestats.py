#############################################################################
#
#
# Module of BFA introducing and managing the Server Stats Interface Class
#
#
#############################################################################
""" This module manages the interface and interactions of the bfa server objects with the statistics of the server.

    Dependencies:

        standalone <- server <- interfacestats
            \
             -> monitoring

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.server import Server
from bfassist.standalone.monitoring import RealTimeRound


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerStatisticsInterface:
    """ The Server Statistics Interface lets a server object interact with the statistics generated on/by it.

        :param server:              The server this interface belongs to.
        :param realTimeRound:       The real time round object containing the information of the current round on the
                                    server.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, realTimeRound: RealTimeRound = None):
        self.server = server
        self.realTimeRound = realTimeRound
