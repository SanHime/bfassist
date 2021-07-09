#############################################################################
#
#
#   Webservice API Request Handling for BFA
#
#
#############################################################################
""" This provides the api request handling functionality for the webservice.

    Dependencies:

        bfassist <- (webservice.)requesthandler <- api
            \
             -> api

        note::  Author(s): Mitch last-check: 07.07.2021 """

import json

from bfassist.webservice.requesthandler import PUT_RequestHandler
from bfassist.api import FunctionApiMixIn


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class API_RequestHandler(PUT_RequestHandler):
    """ The API request handler.

            note::  Author(s): Mitch """

    def do_API_PROCESS(self, api_f: FunctionApiMixIn, parameters: dict):
        """ Performs API request and sends reply of API.

            :param api_f:       The function to call.
            :param parameters:  The arguments to pass to the function as dictionary.

                note::  Author(s): Mitch """

        if parameters is None:
            ret = api_f.func()
        else:
            ret = api_f.func(**parameters)

        self.send_response(200)
        self.end_headers()
        if isinstance(ret, str):
            self.do_SEND_SIMPLE_RESPONSE(ret)
        else:
            self.do_SEND_SIMPLE_RESPONSE(json.dumps(ret))

    def do_API_GET(self, api_f: FunctionApiMixIn, parameters: dict):
        """ Performs API request and sends reply of API.

            :param api_f:       The function to call.
            :param parameters:  The arguments to pass to the function as dictionary.

                note::  Author(s): Mitch """

        self.do_API_PROCESS(api_f, parameters)

    def do_API_PUT(self, api_f: FunctionApiMixIn, parameters: dict):
        """ Performs API request and sends 'reply' of API. PUT requests only return success or failure though.

            :param api_f:       The function to call.
            :param parameters:  The arguments to pass to the function as dictionary.

                note::  Author(s): Mitch """

        self.do_API_PROCESS(api_f, parameters)

    def do_API_POST(self, api_f: FunctionApiMixIn, parameters: dict):
        """ Performs API request and sends 'reply' of API.

            :param api_f:       The function to call.
            :param parameters:  The arguments to pass to the function as dictionary.

                note::  Author(s): Mitch """

        self.do_API_PROCESS(api_f, parameters)

    def do_HANDLE_INVALID_API_REQUEST(self):
        """ Function for handling an invalid request to the API. This means the requested function could not be found
        at the specified location in the API tree.

                note::  Author(s): Mitch """

        self.send_response(400)
        self.end_headers()
        self.do_SEND_SIMPLE_RESPONSE('Bad Request: The API could not handle your request.')
