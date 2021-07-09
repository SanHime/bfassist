#############################################################################
#
#
#   Production definition to the update tab to BFA v.5 standalone
#
#
#############################################################################
""" These are the production instructions for the bfa update view of the webclient.

    Dependencies:

        bfassist <- (standalone.)webclient <- update
            |                       |
            |                       |-> webclient
            |                       \-> bodies
            \                        -> headings
             -> standalone -> webclient -> update -> production @build

        note::  Author(s): Mitch last-edit: last-check: 08.07.2021 """

from bfassist.standalone.webclient.webclient import *
from bfassist.standalone.webclient.bodies import *
from bfassist.standalone.webclient.headings import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


UPDATE_VIEW = View("update", "Update", "Update view of the bfa webclient. Place to check for updates and installing "
                                       "them.")


def build():
    global UPDATE_VIEW
    from bfassist.standalone.webclient.update.production import injectUpdatePort, styleUpdatePort, onLoadFunction

    UPDATE_VIEW.addStyleSheetFromForeignView(ONLINE_VIEW)
    UPDATE_VIEW.addScriptFromForeignView(ONLINE_VIEW)
    UPDATE_VIEW.setTitle("BF-A Web Client Updates")
    UPDATE_VIEW += createH1("BF-A Web Client Setup")
    UPDATE_VIEW += injectUpdatePort(*createClientPort())
    UPDATE_VIEW += styleUpdatePort()

    UPDATE_VIEW.HTML_DOCUMENT.body.properties = {'onload': onLoadFunction.name + "()"}


UPDATE_VIEW.build = build

if __name__ == "__main__":
    UPDATE_VIEW.build()
    UPDATE_VIEW.export()
