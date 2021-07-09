#############################################################################
#
#
#   Base Request Handler network Module to BFA Master
#
#
#############################################################################
""" This module handles base requests from the BFA Client. Comments in this file and the corresponding client file are
used to keep associated client and server functions aligned on the same line of code.

    Dependencies:

        bfassist <- (network.master.)baserequesthandler
            |
            |-> bfa_logging
            \-> references
             -> network

        note::  Author(s): Mitch last-check: 07.07.2021 """

import json
from pathlib import Path
from time import sleep
from socket import timeout
from os.path import getsize
from socketserver import BaseRequestHandler

from bfassist.bfa_logging import log
from bfassist.references import shaForFile
from bfassist.network import BFA_Settings


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


DEFAULT_EXEMPTIONS = {
    '__pycache__',
    'svn-',
    '.db',
    '.ini',
    '.crt',
    '.key',
    '.pem',
    'bfassist/master',
    'bfassist/network/client/leagueclient',
    'bfassist/network/master',
    'bfassist/references/binaries/league',
    'bfassist/references/eventlogs',
    'bfassist/references/maps/league',
    'bfassist/standalone/admin/administrationleague'
}

LEAGUE_EXTENSIONS = {
    'bfassist/network/client/leagueclient',
    'bfassist/references/binaries/league',
    'bfassist/references/maps/league',
    'bfassist/standalone/admin/administrationleague'
}


class ThreadedTCPBaseRequestHandler(BaseRequestHandler):
    """ Request handler for incoming requests to the master server.

        :param configOf:    A dictionary containing client ips as keys and the config they were using when they last
                            connected.
        :param serversOf:   A dictionary containing client ips as keys and global server signatures of the servers on
                            the client when it last connected.

            note:: Author(s): Mitch """

    configOf = {}
    serversOf = {}

    #
    #
    #   # Client connect
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #   # Client disconnect
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    def handle(self):
        """ Handle all requests from here. Don't let them off the hook before the request has been fully handled.
        Otherwise the connection is lost and has to be reestablished.

                note:: Author(s): Mitch """

        data = self.receiveJSON()
        if data and 'CONFIG' in data:
            self.configOf[self.client_address] = data['CONFIG']
            if 'SERVERS' in data:
                self.serversOf[self.client_address] = data['SERVERS']
            self.sendString("Success: Client signature received.")
            self.receiveRemoteCall()

    def receiveRemoteCall(self):
        """ Used to receive a client request for a remote function call.

                note::  Author(s): Mitch """

        data = self.getRequest()
        self.request.settimeout(5)

        if data in self.client_requests:
            self.client_requests[data](self)
        else:
            log('Received data:  ' + data + ' from a client : ' + str(self.client_address) + ' Unknown request type...',
                3)

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    def getRequest(self):
        """ Simple function to get a request (or response). Assumes end of transmission when data wasn't received for
         more than 3 seconds (not necessarily consecutive).

            :return:    The request if any otherwise empty string.

                note::  Author(s): Mitch """

        request = str(self.request.recv(1024), 'utf-8')
        rTimeout = 3
        while request == '' and rTimeout > 0:
            sleep(1)
            request = str(self.request.recv(1024), 'utf-8')
            rTimeout -= 1

        return request

    def getRestOfRequest(self):
        """ Simple function to receive the rest of a request.

            :return:    Rest of the response.

                note::  Author(s): Mitch """

        request = ""
        rPart = ""
        self.request.settimeout(.5)
        try:
            rPart = str(self.request.recv(1024), 'utf-8')
            while rPart is not None and rPart != '':
                request += rPart
                rPart = str(self.request.recv(1024), 'utf-8')
        except timeout:
            rPart = ""
        finally:
            self.request.settimeout(5)
            return request + rPart

    def sendString(self, s: str):
        """ Simple function to transmit a string encoded with utf-8.

            :param s:   The string to send.

                note::  Author(s): Mitch """

        self.request.sendall(bytes(s, 'utf-8'))

    def sendAsJSON(self, message):
        """ Simple function to transmit a message via json in utf-8 encoding given that it's json-encodable.

            :param message: The message to encode and send.

                note::  Author(s): Mitch """

        if isinstance(message, set):
            message = list(message)
        self.request.sendall(bytes(json.dumps(message), 'utf-8'))

    def receiveJSON(self):
        """ Simple function to receive incoming json.

            :return:    The python representation of the incoming json if decodable otherwise None.

                note::  Author(s): Mitch """

        data = self.getRequest()
        data += self.getRestOfRequest()
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            log("Decode error when receiving json: " + str(e))
            return None

    #   # Client handleResponse
    #
    #   Using this space to give a quick overview over the bfa files and how they are supposed to be used.
    #
    #   bfassist -----> api                         ONLY client
    #               |-> certificates                client/master   *
    #               |-> colours                     ONLY client
    #               |-> master                      ONLY master     **
    #               |-> network \-> client          ONLY client             containing leagueclient
    #               |            -> master          ONLY master     **
    #               |-> references ---> binaries    client/master           containing league binaries
    #               |               \-> eventlogs   ONLY master     **
    #               |                -> maps        client/master           containing league maps
    #               |-> sql                         client/master
    #               |-> standalone                  ONLY client             containing administrationleague in admin
    #               |-> usersystem                  ONLY client
    #               |-> webgen                      ONLY client
    #               |-> webservice                  ONLY client
    #               \-> logging                     client/master
    #                -> init                        client/master
    #
    #   The **packages that are ONLY used by the master are exempt when a client syncs with the master server.
    #   Thus, the respective directories are excluded when creating the full folder signature of bfa.
    #   The master SSL certificate located in *certificates is also excluded for the full folder signature.
    #   Files or folders containing league content are only included if the client is using the league-extensions.

    @staticmethod
    def createFolderSignature(fPath: Path, exemptions: list = None):
        """ Creates a 'folder signature' which is a dictionary containing each file with its respective directory
        structure plus their respective sha-256 hash. A list of substrings to exclude when creating the signature can be
        specified. This way certain file types or folders can be exempt from the signature.

            :param fPath:       The path to the folder to create a signature for.
            :param exemptions:  A list of file substrings to ignore.

            :return:            The dictionary containing the signature.

                note::  Author(s): Mitch """

        filtered = {}
        for cPath in fPath.glob('**/*'):
            if not cPath.is_dir() and \
                    (exemptions is None or not any([True if x in str(cPath) else False for x in exemptions])):
                filtered[str(cPath).split(fPath.name)[1] if fPath.name else str(cPath)] = shaForFile(str(cPath))
        return filtered

    def calculateDifferences(self):
        """ Assists the client to calculate a serialised list of files that differ between the version of the client and
         data that should be on the client according to the master. In particular this function will send a full folder
         signature including all files as explained in a comment above. If the client does not run the league-extensions
         they will be exempt from the calculation of the full folder signature.

                note:: Author(s): Mitch """

        clientConfig = self.configOf[self.client_address]

        if 'league-extensions' in clientConfig[BFA_Settings] and clientConfig[BFA_Settings]['league-extensions']:
            fullFolderSignature = self.createFolderSignature(Path('.'),
                                                             list(DEFAULT_EXEMPTIONS.difference(LEAGUE_EXTENSIONS)))
        else:
            fullFolderSignature = self.createFolderSignature(Path('.'), list(DEFAULT_EXEMPTIONS))
        self.sendAsJSON(fullFolderSignature)

    def sendFiles(self):
        """ Send requested files to the client.

                note:: Author(s): Mitch """

        data = self.getRequest()
        data += self.getRestOfRequest()
        log(str(self.client_address) + " asks for " + data, 0)
        client_need = json.loads(data)

        for file in client_need:
            fileSize = getsize(file)
            with open(file, "rb") as f:
                self.request.sendall(bytes("<FILESIZE>" + str(fileSize) + "</FILESIZE>", 'utf-8'))
                self.request.sendfile(f)

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #   # Client getUpdate
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    client_requests = {
        "calculateDifferences": calculateDifferences,
        "getFiles": sendFiles
    }
