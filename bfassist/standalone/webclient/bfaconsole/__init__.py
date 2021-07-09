#############################################################################
#
#
#   Definition to the bfa console to BFA standalone c7
#
#
#############################################################################
""" These are the definitions of the production instructions for the bfa console view of the webclient.

    Dependencies:

        bfassist <- (standalone.)webclient <- bfaconsole
            |                       |
            |                       |-> webclient
            |                       \-> bodies
            \                        -> headings
             -> standalone -> webclient -> bfaconsole -> production @build

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


CONSOLE_VIEW = View("bfaconsole", "BF-A Console", "Console view of the bfa webclient. Base-integration point of all api"
                                                  " based functions.")


def build():
    global CONSOLE_VIEW
    from bfassist.standalone.webclient.bfaconsole.production import injectBFAconsole, styleBFAconsole

    CONSOLE_VIEW.addStyleSheetFromForeignView(ONLINE_VIEW)
    CONSOLE_VIEW.addScriptFromForeignView(ONLINE_VIEW)
    CONSOLE_VIEW.setTitle("BF-A Web Client Console")
    CONSOLE_VIEW += createH1("BF-A Web Client Console")
    CONSOLE_VIEW += injectBFAconsole(*createClientPort())
    CONSOLE_VIEW += styleBFAconsole()


CONSOLE_VIEW.build = build


if __name__ == "__main__":
    CONSOLE_VIEW.build()
    CONSOLE_VIEW.export()
