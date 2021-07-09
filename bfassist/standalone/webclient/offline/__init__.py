#############################################################################
#
#
#   Definition to the offlineView to BFA standalone c7
#
#
#############################################################################
""" These are the definitions of the production instructions for the offlineView of the webclient.

    Dependencies:

        bfassist <- (standalone.)webclient <- offline
            |                       |
            |                       \-> headings
            |                        -> bodies
            \-> webgen
             -> standalone -> webclient -> offline -> production    @build

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.webclient.headings import *
from bfassist.standalone.webclient.bodies import *
from bfassist.webgen import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


OFFLINE_VIEW = View("offline", "Logout",
                    "Offline view on the bfa webclient. That is what the webclient appears like if called when not "
                    "logged in.")


def build():
    global OFFLINE_VIEW
    from bfassist.standalone.webclient.offline.production import createLoginForm, styleLoginForm

    OFFLINE_VIEW.setTitle("BF-A Web Client(offline)")
    OFFLINE_VIEW += STANDARD_HTML_BODY_STYLE
    OFFLINE_VIEW += createH1("BF-A Web Client(offline)")
    OFFLINE_VIEW += createLoginForm()
    OFFLINE_VIEW += styleLoginForm()


OFFLINE_VIEW.build = build


if __name__ == "__main__":
    OFFLINE_VIEW.build()
    OFFLINE_VIEW.export()
