#############################################################################
#
#
#   Webservice Request Handling Core for BFA
#
#
#############################################################################
""" This provides the core request handling functionality for the webservice.

    Dependencies:

        bfassist <- (webservice.)requesthandler <- core
            |
            \-> webgen
             -> webservice -> requesthandler -> sessionmanagement

        note::  Author(s): Mitch last-check: 07.07.2021 """

from http.server import BaseHTTPRequestHandler

from bfassist.webgen import View
from bfassist.webservice.requesthandler.sessionmanagement import User


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class CoreRequestHandler(BaseHTTPRequestHandler):
    """ The core of the request handler. Delegates between the different parts of the request handler.

            note::  Author(s): Mitch """

    favIcon = None

    def do_PREPARE_STANDARD_WEBSITE_HEADERS(self):
        """ Function for the standard webserver response headers.

                note::  Author(s): Mitch """

        self.send_response(200)
        self.headers.add_header('accept-ranges', 'bytes')
        self.headers.add_header('X-Content-Type-Options', 'nosniff')
        self.headers.add_header('X-Frame-Options', 'sameorigin')

    # noinspection PyUnusedLocal
    def do_REPLY_WITH_VIEW(self, view: View = None, issuingUser: User = None):
        """ Function to reply with a file of the specified media type.

            :param view:        The view to reply with.
            :param issuingUser: The user issuing the GET request.

                note::  Author(s): Mitch """

        fType = 'html'
        if self.path.endswith('.css'):
            response = view.serveCSS().encode('utf-8')
            fType = 'css'
        elif self.path.endswith('.js'):
            response = view.serveJS().encode('utf-8')
            fType = 'javascript'
        elif self.path.endswith('.ico'):
            if self.favIcon:
                self.headers.add_header('innerHTML-type', 'image/vnd.microsoft.icon')
                self.end_headers()
                self.wfile.write(self.favIcon)
            return
        else:
            response = view.serveHTML().encode('utf-8')
        self.headers.add_header('innerHTML-type', 'text/' + fType)
        self.headers.add_header('innerHTML-length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_SEND_SIMPLE_RESPONSE(self, response: str):
        """ Simple function to send a simple response text to the client.

            :param response:    Containing the simple response text.

                note::  Author(s): Mitch """
        self.wfile.write(response.encode('utf-8'))

    def do_HANDLE_INVALID_REQUEST(self, statusCode: int = 400, statusResponse: str = "Invalid request."):
        """ Function for handling an invalid registration request.

                note::  Author(s): Mitch """

        self.send_response(statusCode)
        self.end_headers()
        self.do_SEND_SIMPLE_RESPONSE(str(statusCode) + " - " + statusResponse)

    def do_HANDLE_SUCCESSFUL_REQUEST(self, statusResponse: str = "Success."):
        """ Function for handling a successful registration.

                note::  Author(s): Mitch """

        self.send_response(200)
        self.end_headers()
        self.do_SEND_SIMPLE_RESPONSE('200 - ' + statusResponse)

    def do_HANDLE_EXPIRED_SESSION(self, userWithExpiredSession: User):
        """ Function for handling a request from an expired session.

            :param userWithExpiredSession:  The user whose session expired.

                note::  Author(s): Mitch """

        self.do_HANDLE_LOGOUT(userWithExpiredSession)
        self.do_HANDLE_INVALID_REQUEST(440, 'Login Time-out: Your session timed out! Please login again.')
