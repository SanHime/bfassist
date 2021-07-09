#############################################################################
#
#
#   RequestHandler for the bfa webservice
#
#
#############################################################################
""" This provides a request handler for serving API requests and/or webgen Views. In particular it builds the request
handler using some import trickery that's similar to what was done in the network package but less extreme.

    Dependencies:

        requesthandler ---> core
                        |-> authentication
                        |-> get
                        |-> post
                        \-> put
                         -> api

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webservice.requesthandler.core import CoreRequestHandler
from bfassist.webservice.requesthandler.authentication import AuthenticationRequestHandler
from bfassist.webservice.requesthandler.get import GET_RequestHandler
from bfassist.webservice.requesthandler.post import POST_RequestHandler
from bfassist.webservice.requesthandler.put import PUT_RequestHandler
from bfassist.webservice.requesthandler.api import API_RequestHandler


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


RequestHandler = API_RequestHandler
