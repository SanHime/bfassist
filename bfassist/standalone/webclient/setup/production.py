#############################################################################
#
#
#   Production definitions for the setup view to BFA standalone c7
#
#
#############################################################################
""" These are the production instructions for the setup view of the webclient.

    Dependencies:

        bfassist <- standalone <- webclient <- setup <- production
            |           |           |
            |           |           \-> colourscheme
            |           \            -> fonts
            \            -> api
             -> framework ----> html
                            \-> js
                             -> css

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.standalone.webclient.colourscheme import BFA_COLOURS
from bfassist.standalone.webclient.fonts import *
from bfassist.standalone import KERN
from bfassist.webgen.framework.html import *
from bfassist.webgen.framework.js import *
from bfassist.webgen.framework.css import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


getServers = KERN.API.GET_API.getServers.apiMixIn
getServers_constraints = {'BFAName', 'BFPath', 'local_monitoring'}
editServer = KERN.API.PUT_API.editServer.apiMixIn
deleteServer = KERN.API.POST_API.deleteServer.apiMixIn
bfaServersScrollTable = ScrollTable('bfaServers', 'BF-A Servers', getServers.returnTypeHint, (editServer, deleteServer),
                                    getServers_constraints)
getBFAUsers = KERN.API.GET_API.getBFAUsers.apiMixIn
editBFAUser = KERN.API.PUT_API.editBFAUser.apiMixIn
deleteBFAUser = KERN.API.POST_API.deleteBFAUser.apiMixIn
bfaUsersScrollTable = ScrollTable('bfaUsers', 'BF-A Users', getBFAUsers.returnTypeHint, (editBFAUser, deleteBFAUser))
onLoadFunction = JS_Function('setupOnLoad')

createServer = KERN.API.POST_API.createServer.apiMixIn
createBFAUser = KERN.API.POST_API.createBFAUser.apiMixIn

SETUP_PORT = td()
SETUP_PORT.Id = 'setupPort'

INPUT_PORT = InputPort('setup', (createServer, createBFAUser, editServer, editBFAUser, deleteServer, deleteBFAUser))
for inputFunction in INPUT_PORT.inputForms:
    inputForm = INPUT_PORT.inputForms[inputFunction]
    for request in inputForm.script:
        request.callOnSuccess(ScrollTable.getScriptForClearingScrollTables())
        request.callOnSuccess(onLoadFunction)
INPUT_PORT.styleInputPort(BFA_COLOURS.GREY, BFA_COLOURS.SILVER)


def injectSetupPort(clientPortHTML: tuple, clientPortJS: tuple):
    """ Function to inject the setup-port into the client-port.

        :param clientPortHTML:  HTML of the clientPort.
        :param clientPortJS:    JS of the clientPort.

        :return:                Pair of tuples of HTML and JS.

            note::  Author(s): Mitch """

    global SETUP_PORT

    start = KERN.API.PUT_API.start.apiMixIn
    stop = KERN.API.PUT_API.stop.apiMixIn

    SETUP_PORT += bfaUsersScrollTable, bfaServersScrollTable

    Buttons = (ButtonInput("Add", INPUT_PORT.show(createServer, createBFAUser)),
               ButtonInput("Edit", INPUT_PORT.show(editServer, editBFAUser)),
               ButtonInput("Delete", INPUT_PORT.show(deleteServer, deleteBFAUser)),
               ButtonInput("Start"), ButtonInput("Stop"))

    SETUP_PORT += Buttons
    SETUP_PORT += (INPUT_PORT, )

    clientPort = clientPortHTML[0]
    clientPort += SETUP_PORT
    SETUP_PORT.properties['colspan'] = '8'

    getBFAUsersJSf = getBFAUsers.fillScrollTableWithFunctionOutput(bfaUsersScrollTable)
    getBFAUsersJSf.generateJSCode()
    getServersJSf = getServers.fillScrollTableWithFunctionOutput(bfaServersScrollTable)
    getServersJSf.generateJSCode()
    onLoadFunction.addCallsTo(getBFAUsersJSf, getServersJSf)

    startJSf = start.wrapISOwithJavaScript((None, Buttons[3], None))
    startJSf.generateJSCode()
    stopJSf = stop.wrapISOwithJavaScript((None, Buttons[4], None))
    stopJSf.generateJSCode()

    clientPortJS = (
        clientPortJS,
        ScrollTable.getScriptForClearingScrollTable(),
        ScrollTable.getScriptForClearingScrollTables(),
        getBFAUsersJSf,
        getServersJSf,
        onLoadFunction,
        startJSf,
        stopJSf
    )
    clientPortJS += INPUT_PORT.script
    clientPortJS += Form.getScriptsForFillingFormsWithDataForFunctions(editServer, editBFAUser, deleteServer,
                                                                       deleteBFAUser)
    clientPortJS += bfaUsersScrollTable.script
    clientPortJS += bfaServersScrollTable.script

    return clientPortHTML, clientPortJS


def styleSetupPort():
    """ Function that creates the style to be used for the setup-port.

        :return:    Set of CSS Rules containing the style definitions for the setup-port.

            note::  Author(s): Mitch """

    CSS = set()

    styleTypeTarget = SETUP_PORT
    CSS.add(styleTypeTarget.styleThisNode({
        set_vertical_align('top')
    }))

    bfaUsersScrollTable.defineStyleForDataCells(borderColour=BFA_COLOURS.BLUE)
    CSS.update(bfaUsersScrollTable.styles)

    styleTypeTarget = bfaUsersScrollTable
    CSS.add(styleTypeTarget.styleThisNode({
        set_width('600px'),
        set_height('200px')
    }))
    CSS.add(styleTypeTarget.styleThisClass({
        set_border('2px', 'solid', BFA_COLOURS.SILVER),
        set_border_radius('15px'),
        set_padding('5px'),
        set_display('inherit')
    }))

    styleTypeTarget = h2()
    CSS.add(styleTypeTarget.styleThisType({
        set_text_align('center'),
        set_colour(BFA_COLOURS.BLUE.createVariant('faint')),
        set_border('1px', 'solid', BFA_COLOURS.BLUE.createVariant('fainter')),
        set_border_radius('20px'),
        set_font_size('15px'),
        set_margin('0')
    }))

    bfaServersScrollTable.defineStyleForDataCells(borderColour=BFA_COLOURS.BLUE)
    CSS.update(bfaServersScrollTable.styles)

    styleTypeTarget = bfaServersScrollTable
    CSS.add(styleTypeTarget.styleThisNode({
        set_width('540px'),
        set_height('200px')
    }))

    CSS.update(ScrollTable.getAllScrollTableStyles(BFA_COLOURS.LIGHT_GREY, BFA_COLOURS.SLATE_GREY,
                                                   BFA_COLOURS.DARK_GREY))

    styleTypeTarget = button()
    CSS.add(styleTypeTarget.styleThisType({
        set_font_family(Agency_FB, STANDARD_BACKUP_FONTS),
        set_font_size('25px'),
        set_font_weight('bold'),
        set_colour(BFA_COLOURS.BLUE),
        set_border_radius('15px'),
        set_cursor('pointer')
    }))

    styleTypeTarget = INPUT_PORT
    CSS.update(styleTypeTarget.styles)

    return CSS
