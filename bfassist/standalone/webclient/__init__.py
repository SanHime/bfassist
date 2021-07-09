#############################################################################
#
#
#   Webclient Module to BFA c7 Standalone
#
#
#############################################################################
""" This module offers the definitions for the bfa web framework to produce the views required from a web client via
HTTPS GET requests.

    Dependencies:

        webclient ----> offline
                    |-> webclient
                    |-> setup
                    \-> bfaconsole
                     -> update

        note::  Author(s): last-check: 08.07.2021 """

from bfassist.standalone.webclient.offline import OFFLINE_VIEW
from bfassist.standalone.webclient.webclient import ONLINE_VIEW
from bfassist.standalone.webclient.setup import SETUP_VIEW
from bfassist.standalone.webclient.bfaconsole import CONSOLE_VIEW
from bfassist.standalone.webclient.update import UPDATE_VIEW


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


TOP_LEVEL_NAVIGATION_VIEWS = (OFFLINE_VIEW, ONLINE_VIEW, SETUP_VIEW, CONSOLE_VIEW, None, None, None, UPDATE_VIEW)
VIEW_BY_NAME = {None if view is None else view.Name: view for view in TOP_LEVEL_NAVIGATION_VIEWS}
