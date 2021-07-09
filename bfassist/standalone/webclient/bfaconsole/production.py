#############################################################################
#
#
#   Production definitions for the bfa console view to BFA standalone c7
#
#
#############################################################################
""" These are the production instructions for the bfa console view of the webclient.

    Dependencies:

        bfassist <- (standalone.)webclient <- bfaconsole <- production
            |                       \
            |                        -> colourscheme
            |-> framework --\-> html
            \                -> css
             -> standalone  @injectBFAconsole

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.webclient.colourscheme import BFA_COLOURS
from bfassist.webgen.framework.html import *
from bfassist.webgen.framework.css import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


CONSOLE = Console('bfa')
CONSOLE_PORT = td()
CONSOLE_PORT.Id = 'consolePort'


def injectBFAconsole(clientPortHTML: tuple, clientPortJS: tuple):
    """ Function to inject the bfa-console into the client-port.

        :param clientPortHTML:  HTML of the clientPort.
        :param clientPortJS:    JS of the clientPort.

            note::  Author(s): Mitch """

    from bfassist.standalone import KERN
    global CONSOLE

    clientPort = clientPortHTML[0]
    CONSOLE.installAPI(KERN.API.by_modules)
    CONSOLE.setHeight('500px')
    CONSOLE.setInputBorderColour(BFA_COLOURS.LIGHT_GREY)
    CONSOLE_PORT.appendChildNode(CONSOLE)
    clientPort += CONSOLE_PORT
    CONSOLE_PORT.properties['colspan'] = '8'

    clientPortJS = (
        CONSOLE.script,
        clientPortJS
    )

    return clientPortHTML, clientPortJS


def styleBFAconsole():
    """ Function that creates the style to be used for the bfa-console.

        :return:    Set of CSS Rules containing the style definitions for the setup-port.

            note::  Author(s): Mitch """

    CSS = set()

    styleTypeTarget = CONSOLE_PORT
    CSS.add(styleTypeTarget.styleThisNode({
        set_width('100%'),
        set_height('100%')
    }))

    CSS.update(CONSOLE.styles)
    return CSS
