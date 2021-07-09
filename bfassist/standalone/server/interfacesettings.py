#############################################################################
#
#
# Module of BFA introducing and managing the Server Settings Interface Class
#
#
#############################################################################
""" This module manages the interface and interactions of the bfa server objects with the settings of the server.

    Dependencies:

        standalone <- server <- interfacesettings
            \
             -> monitoring

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.server import Server
from bfassist.standalone.monitoring import BfServerSetting


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerSettingsInterface:
    """ The Server Settings Interface lets a server object interact with the settings used on it.

        :param server:              The server this interface belongs to.
        :param settings:            The bf server settings object that corresponds with the settings currently on the
                                    server.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, settings: BfServerSetting = None):
        self.server = server
        self.settings = settings
