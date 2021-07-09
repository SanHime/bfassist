#############################################################################
#
#
#   Webclient Bodies Module to BFA c7 Standalone
#
#
#############################################################################
""" This module makes bodies/body-styles used in the webclient available.

    Dependencies:

        bfassist <- standalone <- webclient <- bodies
            |           |           |
            |           |           \-> colourscheme
            |           \            -> fonts
            |            -> api
            |-> webgen-> framework -\-> css
            \                        -> html
             -> standalone  @createClientPort
                    \
                     -> webclient   @createTopNavigation

        note::  Author(s): last-check: 08.07.2021 """

from bfassist.standalone.webclient.colourscheme import BFA_COLOURS
from bfassist.standalone.webclient.fonts import Agency_FB, STANDARD_BACKUP_FONTS
from bfassist.standalone.api import BFA_FunctionApiMixIn
from bfassist.webgen import View
from bfassist.webgen.framework.css import *
from bfassist.webgen.framework.html import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


STANDARD_HTML_BODY_STYLE = body().styleThisType({set_background_colour(BFA_COLOURS.GREY),
                                                 set_padding('1%', '5%', '5%', '5%'),
                                                 set_font_family(Agency_FB, STANDARD_BACKUP_FONTS),
                                                 set_colour(BFA_COLOURS.BLUE)})

CLIENT_PORT = None
TOP_NAVIGATION = None

LOGOUT_NAVIGATION_HEADER = th()
LOGOUT_NAVIGATION_HEADER.Id = 'logoutNavigationHeader'

LOGOUT_PSEUDO_BUTTON = PseudoButtonInput()
LOGOUT_PSEUDO_BUTTON.Id = 'logoutPseudoButton'


def createClientPort():
    """ Function that creates the client-port using a table layout.

        :return:    HTML and JS for the client-port.

            note::  Author(s): Mitch """

    global CLIENT_PORT, TOP_NAVIGATION
    from bfassist.standalone import KERN

    logout = KERN.API.PUT_API.logoutBFAUser.apiMixIn

    TOP_NAVIGATION = createTopNavigation(logout)
    JS = LOGOUT_PSEUDO_BUTTON.onClick

    portBody = TableBody.fromRowAndColumnCount(1, 0)
    CLIENT_PORT = Table((TOP_NAVIGATION, ), (portBody, ))
    CLIENT_PORT.Id = 'clientPort'

    HTML = CLIENT_PORT

    return HTML, JS


def createTopNavigation(logout: BFA_FunctionApiMixIn):
    """ Function that creates the top navigation bar of the client port.

        :return:    HTML of the top navigation bar.

            note::  Author(s): Mitch """
    from bfassist.standalone.webclient import TOP_LEVEL_NAVIGATION_VIEWS

    size = len(TOP_LEVEL_NAVIGATION_VIEWS)
    navigation = TableHead.fromRowAndColumnCount(1, size)
    navigation[0].Id = "clientPortTopNavigation"
    for x in range(size):
        viewToNavigateTo = TOP_LEVEL_NAVIGATION_VIEWS[x]
        if viewToNavigateTo is None:
            pass
        else:
            navigationElement = navigation[0][x]
            if viewToNavigateTo.Name == 'offline':
                navigationElement.Id = LOGOUT_NAVIGATION_HEADER.Id
                navigationElement += LOGOUT_PSEUDO_BUTTON
                logoutRequest = logout.wrapISOwithJavaScript((None, LOGOUT_PSEUDO_BUTTON, None), '/logout', 'Logout')
                logoutRequest.generateJSCode()
            else:
                navigationElement += a(viewToNavigateTo.DisplayName)
            navigationElement.a.properties['href'] = '../' + viewToNavigateTo.Name

    return navigation


def styleClientPort():
    """ Function that creates the style to be used for the client-port.

        :return:    Set of CSS Rules containing the style definitions for the client-port.

            note::  Author(s): Mitch """

    CSS = set()

    styleTypeTarget = a()
    CSS.add(styleTypeTarget.styleThisType({
        set_display('block'),
        set_text_decoration('none'),
        set_colour(BFA_COLOURS.GREEN.toRGB()),
        set_cursor('pointer'),
        set_font_size('25px'),
        set_font_weight('bold')
    }))

    styleTypeTarget = LOGOUT_PSEUDO_BUTTON
    CSS.add(styleTypeTarget.styleThisNode({
        set_colour(BFA_COLOURS.RED.toRGB()),
        set_cursor('pointer')
    }))

    styleTypeTarget = CLIENT_PORT
    CSS.add(styleTypeTarget.styleThisNode({
        set_border('5px', 'solid', BFA_COLOURS.MIDNIGHT_BLUE),
        set_border_radius('25px'),
        set_width('1200px'),
        set_height('600px'),
        set_margin('auto'),
        set_text_align('center')
    }))

    styleTypeTarget = TOP_NAVIGATION[0]
    CSS.add(styleTypeTarget.styleThisNodesSubType('th', {
        set_border('2px', 'solid', BFA_COLOURS.GREEN.toRGB()),
        set_height('30px'),
        set_font_weight('bold'),
        set_border_radius('20px'),
        set_width('12.5%')
    }))

    CSS.add(styleTypeTarget.styleThisNodesSubNode('th', 'logoutNavigationHeader', {
        set_border('2px', 'solid', BFA_COLOURS.RED.toRGB())
    }))

    return CSS
