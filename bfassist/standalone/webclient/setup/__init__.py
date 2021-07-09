#############################################################################
#
#
#   Definition to the setup view to BFA standalone c7
#
#
#############################################################################
""" These are the definitions of the production instructions for the setup view of the webclient.

    Dependencies:

        bfassist <- (standalone.)webclient <- setup
            |                       |
            |                       |-> webclient
            |                       \-> bodies
            \                        -> headings
             -> standalone -> webclient -> setup -> production  @build

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.webclient.webclient import *
from bfassist.standalone.webclient.bodies import *
from bfassist.standalone.webclient.headings import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


SETUP_VIEW = View("setup", "Setup", "Setup view of the bfa webclient. Section for adding/editing/deleting"
                                    " servers or users.")


def build():
    global SETUP_VIEW
    from bfassist.standalone.webclient.setup.production import injectSetupPort, styleSetupPort, onLoadFunction

    SETUP_VIEW.addStyleSheetFromForeignView(ONLINE_VIEW)
    SETUP_VIEW.addScriptFromForeignView(ONLINE_VIEW)
    SETUP_VIEW.setTitle("BF-A Web Client(online)")
    SETUP_VIEW += createH1("BF-A Web Client Setup")
    SETUP_VIEW += injectSetupPort(*createClientPort())
    SETUP_VIEW += styleSetupPort()

    SETUP_VIEW.HTML_DOCUMENT.body.properties = {'onload': onLoadFunction.name + "()"}


SETUP_VIEW.build = build


if __name__ == "__main__":
    SETUP_VIEW.build()
    SETUP_VIEW.export()
