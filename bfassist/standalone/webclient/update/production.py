#############################################################################
#
#
#   Production definitions for the update view to BFA standalone c7
#
#
#############################################################################
""" These are the production instructions for the update view of the webclient.

    Dependencies:

        bfassist <- standalone <- (webclient.update.)production
            \
             -> webgen ---> html
                        \-> js
                         -> css

        note::  Author(s): Mitch last-check: 08.07.2021 """

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


getUpdate = KERN.API.GET_API.getUpdate.apiMixIn
getAutoUpdateSetting = KERN.API.GET_API.getAutoUpdateSetting
getAutoUpgradeSetting = KERN.API.GET_API.getAutoUpgradeSetting
getLeagueExtensionAvailability = KERN.API.GET_API.getLeagueExtensionAvailability

bfaUpdate = KERN.API.POST_API.bfaUpdate
bfaUpgrade = KERN.API.POST_API.bfaUpgrade

toggleAutoUpdateSetting = KERN.API.PUT_API.toggleAutoUpdateSetting
toggleAutoUpgradeSetting = KERN.API.PUT_API.toggleAutoUpgradeSetting

onLoadFunction = JS_Function('updateOnLoad')

UPDATE_PORT = td()
UPDATE_PORT.Id = 'updatePort'


def injectUpdatePort(clientPortHTML: tuple, clientPortJS: tuple):
    """ Function to inject the update-port into the client-port.

        :param clientPortHTML:  HTML of the clientPort.
        :param clientPortJS:    JS of the clientPort.

        :return:                Pair of tuples of HTML and JS.

            note::  Author(s): Mitch """

    global UPDATE_PORT

    clientPort = clientPortHTML[0]
    clientPort += UPDATE_PORT
    UPDATE_PORT.properties['colspan'] = '8'

    return clientPortHTML, clientPortJS


def styleUpdatePort():
    """ Function that creates the style to be used for the update-port.

        :return:    Set of CSS Rules containing the style definitions for the update-port.

            note::  Author(s): Mitch """

    CSS = set()
    return CSS
