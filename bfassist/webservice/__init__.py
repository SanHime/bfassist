#############################################################################
#
#
#   Webservice for BFA
#
#
#############################################################################
""" This provides a simple web-server that can support a REST-like HTTPS API communication with authentication based on
the bfa user system. In fact we only implement GET/PUT/POST HTTPS method hooks and leave the actual api integration to
be customised. The authentication is mandatory by default and once authenticated the webservice also supports replying
with Views of the bfa webgen on GET requests.

API functions and Views should not have the same 'name', otherwise Views will be treated with priority by default.

    Dependencies:

        bfassist <- webservice
            |
            |-> bfa_logging
            \-> certificates
             -> webservice -> requesthandler

        note::  Author(s): Mitch last-check: 07.07.2021 """

from os.path import exists
from http.server import ThreadingHTTPServer
from uuid import getnode
from random import randint
from ssl import wrap_socket

from bfassist.bfa_logging import log
from bfassist.certificates import generateCert
from bfassist.webservice.requesthandler import RequestHandler


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


# noinspection PyTypeChecker
class WebService:
    """ Python implementation of a webservice.

        :param httpd:       Standard python http server with threading capability.
        :param listenName:  The hostname/IP the webservice will be listening on.
        :param listenPort:  The port we listen on. Using non-standard to (1) avoid collisions with a possible
                            other web server running on our machine (2) make ourselves a little harder to find.
        :param pemchain:    The server key/cert-chain. The cert is usually self-signed so not really a chain.
        :param rest:        The request handler of the server.
        :param running:     A flag that indicates if the service is currently running.

            note::  Author(s): Mitch """

    def __init__(self, httpd: ThreadingHTTPServer = None, listenName: str = 'localhost', listenPort: int = 444,
                 pemchain: str = None, requestHandler: RequestHandler = RequestHandler, domain: str = None,
                 running: bool = False):

        self.domain = domain
        self.requestHandler = requestHandler
        self.listenName = listenName
        self.listenPort = listenPort
        self.running = running
        if httpd is None:
            self.httpd = ThreadingHTTPServer((self.listenName, self.listenPort), self.requestHandler)
        else:
            self.httpd = httpd

        if pemchain:
            self.pemchain = pemchain
        elif not exists('bfassist/certificates/standalone_bfa.pem'):
            log('No certificate found. Generating a new one.', 1)
            self.pemchain = generateCert('admin@bfa.net', 'BF-A', 'eu', '-', '-', 'BF-A', str(getnode()),
                                         randint(0, 2 ** 16 - 1), 0, pem="standalone")
        else:
            self.pemchain = 'bfassist/certificates/standalone_bfa.pem'

    def run(self):
        """ Function to start the web service in its own thread.

                note::  Author(s): Mitch """

        self.httpd.socket = wrap_socket(self.httpd.socket, certfile=self.pemchain, server_side=True)
        self.requestHandler.sessionManager.start()
        self.httpd.serve_forever()
        self.running = True

    def stop(self):
        """ Function to gracefully stop the entire web service.

                note::  Author(s): Mitch """

        self.requestHandler.sessionManager.stopper = True
        self.requestHandler.sessionManager.join(15)
        self.httpd.server_close()
        self.running = False
