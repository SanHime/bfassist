#############################################################################
#
#
#   Production definitions for the offline view to BFA standalone c7
#
#
#############################################################################
""" These are the production instructions for the offline view of the webclient.

    Dependencies:

        bfassist <- standalone <- webclient <- offline <- production
            |           |           |
            |           |           \-> colourscheme
            |           \            -> fonts
            \            -> api
             -> framework -> html

        note::  Author(s): Mitch last-edit: last-check: 08.07.2021 """

from bfassist.standalone.webclient import ONLINE_VIEW
from bfassist.standalone.webclient.colourscheme import BFA_COLOURS
from bfassist.standalone.webclient.fonts import Agency_FB, STANDARD_BACKUP_FONTS
from bfassist.standalone import KERN
from bfassist.standalone.api import BFA_FunctionApiMixIn
from bfassist.webgen.framework.html import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def createLoginForm():
    """ Function that creates the login form to be used by the offline view.

        :return:    Tuple of HTML containing the login form and tuple of wrapping JS.

            note::  Author(s): Mitch """

    register = KERN.API.PUT_API.registerBFAUser.apiMixIn
    login = KERN.API.PUT_API.loginBFAUser.apiMixIn

    loginForm = Form('login')
    loginForm += Fieldset('loginAndRegister')

    registerISO = register.generateSimpleISO()
    loginForm.fieldset.Input += registerISO[0]
    loginForm.fieldset.Submit += registerISO[1]
    registerRequest = register.wrapISOwithJavaScript(registerISO, '/register', 'Register')
    registerRequest.generateJSCode()

    loginISO = registerISO[0], login.generateSimpleISO()[1], registerISO[2]
    loginForm.fieldset.Submit += loginISO[1]
    loginRequest = login.wrapISOwithJavaScript(loginISO, '/login', 'Login')
    loginRequest.generateJSCode()
    loginRequest.redirectOnSuccess(ONLINE_VIEW)

    HTML = loginForm, registerISO[2]
    JS = registerRequest, loginRequest

    return HTML, JS


def styleLoginForm():
    """ Function that creates the style to be used for the login form of this offline view.

        :return:    Set of CSS Rules containing the style definitions for the login form.

            note::  Author(s): Mitch """

    CSS = set()

    styleTypeTarget = fieldset()
    CSS.add(styleTypeTarget.styleThisType({
        set_position('absolute'),
        set_top('50%'),
        set_left('50%'),
        set_transform('-50%', '-50%'),
        set_margin_bottom('15px'),
        set_colour(BFA_COLOURS.BLUE),
        set_width('400px'),
        set_font_weight('bold')
    }))

    styleTypeTarget = button()
    CSS.add(styleTypeTarget.styleThisType({
        set_font_size('25px'),
        set_colour(BFA_COLOURS.BLUE),
        set_border_radius('15px'),
        set_font_family(Agency_FB, STANDARD_BACKUP_FONTS),
        set_cursor('pointer')
    }))

    styleTypeTarget = div()
    CSS.add(styleTypeTarget.styleThisType({
        set_colour(BFA_COLOURS.RED),
        set_text_align('center'),
        set_font_size('25px')
    }))
    return CSS
