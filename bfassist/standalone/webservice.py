#############################################################################
#
#
#   Web service to BFA c7 Standalone
#
#
#############################################################################
""" This module will refit the bfa webservice so that it serves the fulfills all purposes of the bfa standalone.

    Dependencies:

        bfassist <- (standalone.)webservice
            |
            |-> webservice -> requesthandler -> sessionmanagement
            |-> standalone -\-> api
            |                -> webclient
            \-> network
             -> standalone  @BFA_API_RequestHandler.extractFunctionFromRequest

        note::  Author(s): last-check: 08.07.2021 """

import json

from bfassist.webservice import WebService
from bfassist.webservice.requesthandler import RequestHandler
from bfassist.webservice.requesthandler.sessionmanagement import User
from bfassist.standalone.api import BFA_FunctionApiMixIn
from bfassist.standalone.webclient import OFFLINE_VIEW, VIEW_BY_NAME
from bfassist.network import CONFIG, BFA_Settings


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BFA_API_RequestHandler(RequestHandler):
    """ The API request handler.

            note::  Author(s): Mitch """

    with open('bfassist/webservice/BFA_1.ico', 'rb') as icoFile:
        favIcon = icoFile.read()

    def extractParametersFromRequest(self):
        """ Function that extracts potential parameters from the request body.

            :return:    Dictionary {param1: value1}.

                note::  Author(s): Mitch """

        content_length = int(self.headers['Content-Length'])
        parameters = {}
        if content_length > 0:
            body = self.rfile.read(content_length)
            parameters = json.loads(body)

        return parameters

    @staticmethod
    def extractParametersFromGETRequest(potentialParameters: str):
        """ Function that extracts potential parameters included with a GET request.

            :param potentialParameters: A str of potential parameters params?param1=value1&param2=value2....

            :return:                    Called API function and Dictionary {param1: value1}.

                note::  Author(s): Mitch """

        parameters = {}
        if 'params?' in potentialParameters:
            potentialParameters = potentialParameters[len('params?'):]
            parameterList = potentialParameters.split('&')
            for parameter in parameterList:
                key, value = parameter.split('=')
                parameters[key] = value

        return parameters

    def extractFunctionFromRequest(self, potentialAPIcall: list):
        """ Function that extracts a potential function to call in the API from a GET request.

            :param potentialAPIcall:    A hierarchical list of modules and submodules containing the function to call.

                note::  Author(s): Mitch """

        from bfassist.standalone import KERN

        func = KERN.API.by_modules

        while potentialAPIcall:
            currentLevel = potentialAPIcall.pop(0)
            if currentLevel not in func:
                self.do_HANDLE_INVALID_API_REQUEST()
                return None
            else:
                func = func[currentLevel]

        if isinstance(func, BFA_FunctionApiMixIn):
            return func
        else:
            return None


RequestHandler = BFA_API_RequestHandler


class BFA_GET_RequestHandler(RequestHandler):

    Views = VIEW_BY_NAME

    def do_HANDLE_UNAUTHORIZED_GET_REQUEST(self):
        """ Function for handling an unauthorized GET request.

                note::  Author(s): Mitch """

        self.do_PREPARE_STANDARD_WEBSITE_HEADERS()
        self.do_REPLY_WITH_VIEW(OFFLINE_VIEW, None)

    # noinspection PyUnusedLocal
    def do_PROCESS_POTENTIAL_API_GET_REQUEST(self, issuingUser: User):
        """ Function for processing a potential API GET request.

            :param issuingUser: The user issuing the PUT request.

                note::  Author(s): Mitch """

        potentialAPIcall = self.path.split('/')[1:]
        potentialParameters = potentialAPIcall[-1]
        parameters = self.extractParametersFromGETRequest(potentialParameters)
        if parameters:
            potentialAPIcall = potentialAPIcall[:-1]
        func = self.extractFunctionFromRequest(potentialAPIcall)
        if func is None:
            self.do_HANDLE_INVALID_API_REQUEST()
        else:
            self.do_API_GET(func, parameters)


RequestHandler = BFA_GET_RequestHandler


class BFA_POST_RequestHandler(RequestHandler):

    # noinspection PyUnusedLocal
    def do_PROCESS_POTENTIAL_API_POST_REQUEST(self, issuingUser: User):
        """ Function for processing a potential API POST request.

            :param issuingUser: The user issuing the PUT request.

                note::  Author(s): Mitch """

        potentialAPIcall = self.path.split('/')[1:]
        parameters = self.extractParametersFromRequest()
        func = self.extractFunctionFromRequest(potentialAPIcall)
        if func is None:
            self.do_HANDLE_INVALID_API_REQUEST()
        else:
            self.do_API_POST(func, parameters)


RequestHandler = BFA_POST_RequestHandler


class BFA_PUT_RequestHandler(RequestHandler):

    # noinspection PyUnusedLocal
    def do_PROCESS_POTENTIAL_API_PUT_REQUEST(self, issuingUser: User):
        """ Function for processing a potential API PUT request.

            :param issuingUser: The user issuing the PUT request.

                note::  Author(s): Mitch """

        potentialAPIcall = self.path.split('/')[1:]
        parameters = self.extractParametersFromRequest()
        func = self.extractFunctionFromRequest(potentialAPIcall)
        if func is None:
            self.do_HANDLE_INVALID_API_REQUEST()
        else:
            self.do_API_PUT(func, parameters)


RequestHandler = BFA_PUT_RequestHandler

# noinspection PyTypeChecker
if BFA_Settings in CONFIG:
    BFA_WEBSERVICE = WebService(listenName=CONFIG[BFA_Settings]['hostname'],
                                pemchain=CONFIG[BFA_Settings]['certificate'],
                                requestHandler=RequestHandler)
else:
    BFA_WEBSERVICE = WebService(requestHandler=RequestHandler)
