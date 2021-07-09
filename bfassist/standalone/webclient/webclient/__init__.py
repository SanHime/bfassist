#############################################################################
#
#
#   Definition to the onlineView/webclient to BFA standalone c7
#
#
#############################################################################
""" These are the definitions of the production instructions for the main online View of the webclient.

    Dependencies:

        bfassist <- (standalone.)webclient <- webclient
            |                       |
            |                       \-> headings
            \                        -> bodies
             -> webgen

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.webclient.headings import *
from bfassist.standalone.webclient.bodies import *
from bfassist.webgen import View


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


ONLINE_VIEW = View('webclient', "Main", "Main online(when logged in) view of the bfa webclient.")


def build():
    global ONLINE_VIEW

    ONLINE_VIEW.setTitle("BF-A Web Client(online)")
    ONLINE_VIEW += STANDARD_HTML_BODY_STYLE
    ONLINE_VIEW += createH1("BF-A Web Client(online)")
    ONLINE_VIEW += BFA_GREEN_CENTERED_H1
    ONLINE_VIEW += createClientPort()
    ONLINE_VIEW += styleClientPort()


ONLINE_VIEW.build = build

if __name__ == "__main__":
    ONLINE_VIEW.build()
    ONLINE_VIEW.export()
