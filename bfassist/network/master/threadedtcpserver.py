#############################################################################
#
#
#   Threaded TCP Server network Module to BFA Master
#
#
#############################################################################
""" This module provides a threaded tcp server for answering requests coming in from bfa clients using SSL-encryption.

    Dependencies:

        bfassist <- (network.master.)threadedtcpserver
            |
            |-> bfa_logging
            \-> certificates
             -> network -> master

        note::  Author(s): Mitch last-check: 07.07.2021 """

from threading import Thread
from os.path import exists
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
from uuid import getnode
from random import randint
from ssl import wrap_socket

from bfassist.bfa_logging import log
from bfassist.certificates import generateCert


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class SecureTCPServer(TCPServer):
    """ Extension to wrap the standard TCPServer into TLS-Encryption. Creates a certificate on the fly
    if none is present.

        :param server_address:      The address the server will listen on.
        :param RequestHandlerClass: The class that will handle the incoming requests.
        :param bind_and_activate:   A flag that indicates the server should be bound and activated from the get-go.
        :param pemchain:            The server key/cert-chain. The cert is usually self-signed so not really a chain.

            note:: Author(s): Mitch """

    pemchain = None

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):

        super(SecureTCPServer, self).__init__(server_address, RequestHandlerClass, bind_and_activate)
        if self.pemchain:
            self.pemchain = pemchain
        elif not exists('bfassist/certificates/master_bfa.pem'):
            log('No certificate found. Generating a new one.', 1)
            self.pemchain = generateCert('admin@bfa.net', 'BF-A', 'eu', '-', '-', 'BF-A', str(getnode()),
                                         randint(0, 2 ** 16 - 1), 0, pem="master")
        else:
            self.pemchain = 'bfassist/certificates/master_bfa.pem'
        self.socket = wrap_socket(self.socket, certfile=self.pemchain, server_side=True)


class ThreadedMasterTCPServer(ThreadingMixIn, SecureTCPServer):
    """ We need to create this to enable request-handling in separate threads so we don't get blocking behaviour.

            note:: Author(s): Mitch """
    pass


class BFA_ThreadedMasterTCPServer:
    """ We need to create this to enable request-handling in separate threads so we don't get blocking behaviour.

        :param host:                The host name (or ip) to listen on.
        :param port:                The port to listen on.
        :param pemchain:            The server key/cert-chain. The cert is usually self-signed so not really a chain.
        :param RequestHandlerClass: The class to handle the incoming requests.
        :param server:              The actual server object.
        :param server_thread:       The thread the server will run on.

            note:: Author(s): Mitch """

    def __init__(self, host: str, port: int, pemchain: str = None, RequestHandlerClass: BaseRequestHandler = None,
                 server: ThreadedMasterTCPServer = None, server_thread: Thread = None):
        from bfassist.network.master import ThreadedTCPRequestHandler

        self.host = host
        self.port = port
        self.pemchain = pemchain
        SecureTCPServer.pemchain = self.pemchain

        if RequestHandlerClass:
            self.RequestHandlerClass = RequestHandlerClass
        else:
            self.RequestHandlerClass = ThreadedTCPRequestHandler
        if server:
            self.server = server
        else:
            self.server = ThreadedMasterTCPServer((self.host, self.port), self.RequestHandlerClass)

        if server_thread:
            self.server_thread = server_thread
        else:
            self.server_thread = Thread(target=self.server.serve_forever)

    def startup(self):
        """ Simple startup function for the master to start serving.

                note:: Author(s): Mitch """

        self.server_thread.start()

        log("Master server running.")

    def shutdown(self):
        """ Simple shutdown function for the master to stop serving.

                note:: Author(s): Mitch """

        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()
        del self
