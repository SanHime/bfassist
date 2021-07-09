#############################################################################
#
#
#   Base Client network Client Module to BFA c7
#
#
#############################################################################
""" This module defines the base client for making requests to the bfa master. Comments in this file and the
corresponding server file are used to keep associated client and server functions aligned on the same line of code.

    Dependencies:

        bfassist <- (network.client.)baseclient
            |
            |-> network
            |-> bfa_logging
            |-> references
            \-> network -> client   @BFABaseClient.connect
             -> standalone          @BFABaseClient.sendClientSignature

        note::  Author(s): Mitch last-check: 09.07.2021 """

import json
from pathlib import Path
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, timeout
from ssl import wrap_socket
from os.path import exists

from bfassist.network import CONFIG
from bfassist.bfa_logging import log
from bfassist.references import shaForFile


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass
#   # Server Full Folder Signature Exemptions
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
#   # Server League Extensions
#
#
#
#
#


class BFABaseClient:
    """ Class that models the client in communication with the master.

        :param client_socket:   Socket the client uses for communication, encrypted with TLS encryption.
        :param connected:       Flag if currently connected to the master.

            note:: Author(s): Mitch """

    def __init__(self, client_socket: socket = None, connected=False):

        if client_socket:
            self.clientSocket = client_socket
        else:
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket = wrap_socket(self.clientSocket, server_side=False)
        self.connected = connected

    def connect(self):
        """ Simple function to connect to the master.

                note:: Author(s): Mitch """

        from bfassist.network.client import BFA_MASTER_IP, BFA_MASTER_PORT

        try:
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket = wrap_socket(self.clientSocket, server_side=False)
            self.clientSocket.connect((BFA_MASTER_IP, BFA_MASTER_PORT))
            self.connected = True

        except ConnectionRefusedError:
            sleep(1)
            self.disconnect()
            sleep(1)
            self.connect()

        except OSError:
            sleep(1)
            self.disconnect()
            log("Required network is unavailable.", 3)

    def disconnect(self):
        """ Simple function to disconnect from the master.

                note::  Author(s): Mitch """
        try:
            self.clientSocket.shutdown(SHUT_RDWR)
            self.clientSocket.close()
            self.connected = False
        except OSError:
            self.clientSocket.close()
            self.connected = False

    def sendClientSignature(self):
        """ Function to send a dictionary containing some information about this client. In particular:
        The stage, branch and revision installed on this client, if the league extensions are active and the global
        dictionary representations/signatures of the managed servers if there are any.

            note::  Author(s): Mitch """
        from bfassist.standalone import KERN

        self.sendAsJSON({'CONFIG': CONFIG, 'SERVERS': KERN.getServerSignatures()})
        if self.getResponse() == "Success: Client signature received.":
            pass
        else:
            raise ConnectionError("Transmission of client signature failed.")

    def declareRemoteCall(self, rfName: str, failure: str = ""):
        """ Used to declare a remote call of a function on the bfa master.

            :param rfName:  The name of the function to call on the bfa master.
            :param failure: Log message in case of failure.

            :return:        True if processed as expected, false otherwise.

                note::  Author(s): Mitch """

        if self.connected:
            try:
                self.clientSocket.settimeout(5)
                self.sendClientSignature()
                self.sendString(rfName)
                return True
            except TimeoutError:
                log(failure + "(TIMEOUT)", 3)
                self.disconnect()
                return False
            except BrokenPipeError:
                self.connected = False
                self.connect()
                return self.declareRemoteCall(rfName, failure)
            except ConnectionError:
                log("Transmission of client signature failed!", 4)
                self.disconnect()
                return False
        else:
            self.connect()
            return self.declareRemoteCall(rfName, failure)

    def getResponse(self):
        """ Simple function to get a response. Assumes end of transmission when data wasn't received for more than 3
         seconds (not necessarily consecutive).

            :return:    The response if any otherwise empty string.

                note::  Author(s): Mitch """

        response = str(self.clientSocket.recv(1024), 'utf-8')
        timeOut = 3
        while response == '' and timeOut > 0:
            sleep(1)
            response = str(self.clientSocket.recv(1024), 'utf-8')
            timeOut -= 1

        return response

    def getRestOfResponse(self):
        """ Simple function to receive the rest of a response.

            :return:    Rest of the response.

                note::  Author(s): Mitch """

        response = ""
        rPart = ""
        self.clientSocket.settimeout(.5)
        try:
            rPart = str(self.clientSocket.recv(1024), 'utf-8')
            while rPart is not None and rPart != '':
                response += rPart
                rPart = str(self.clientSocket.recv(1024), 'utf-8')
        except timeout:
            rPart = ""
        finally:
            self.clientSocket.settimeout(5)
            return response + rPart

    def sendString(self, s: str):
        """ Simple function to transmit a string encoded with utf-8.

            :param s:   The string to send.

                note::  Author(s): Mitch """

        self.clientSocket.sendall(bytes(s, 'utf-8'))

    def sendAsJSON(self, message):
        """ Simple function to transmit a message via json in utf-8 encoding given that it's json-encodable.

            :param message: The message to encode and send.

                note::  Author(s): Mitch """

        if isinstance(message, set):
            message = list(message)
        self.clientSocket.sendall(bytes(json.dumps(message), 'utf-8'))

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

    def handleResponse(self, expected: str, success: str = '', failure: str = ''):
        """ Standardised way to handle a response.

            :param expected:    The expected response.
            :param success:     What to log in case of success.
            :param failure:     What to log in case of failure.

            :return:            True if received expected response, false otherwise.

                note::  Author(s): Mitch """
        response = self.getResponse()

        if response == expected:
            if success:

                log(success, 1)
            self.disconnect()
            return True

        else:
            if failure:

                log(failure, 3)
            self.disconnect()
            return False

    @staticmethod
    def compareClientWith(serverSide: dict):
        """ Function to compare the client side files with a folder signature sent by the server.

            :param serverSide:  Dictionary containing the signature of a folder on the server.

            :return:            List of files on the client side that don't match.

                note::  Author(s): Mitch """

        matches = set()
        for file in serverSide:
            if Path(file).exists():
                sha = shaForFile(file)
                if serverSide[file] == sha:
                    matches.add(file)
        for match in matches:
            serverSide.pop(match)
        return set(serverSide.keys())

    def calculateDifferences(self):
        """ This function calculates the difference of the global master client files with the one found on this local
        client.

            :return:    A list of all files/directories that are out of date with the global master client files.

                note:: Author(s): Mitch """

        if not self.declareRemoteCall('calculateDifferences'):
            return False

        response = self.getResponse()
        response += self.getRestOfResponse()
        self.disconnect()
        serverside = json.loads(response)
        return self.compareClientWith(serverside)

    def getFiles(self, update_list: set = None):
        """ Function to update a list of specified files.

            :param update_list: List of files to be updated.

                note:: Author(s): Mitch """

        if update_list is False:
            return False

        if not self.declareRemoteCall('getFiles'):
            return False

        self.sendAsJSON(list(update_list))

        firstPackets = b''
        firstPacketsAsString = ''

        for file in update_list:
            if not Path('./' + file).parent.exists():
                Path('./' + file).parent.mkdir(parents=True)

            while "</FILESIZE>" not in firstPacketsAsString:
                firstPackets += self.clientSocket.recv(1024)
                firstPacketsAsString = str(firstPackets, 'utf-8', errors='ignore')

            fileSizeStart = firstPacketsAsString.index('<FILESIZE>') + len('<FILESIZE>')
            fileSizeEnd = firstPacketsAsString.index('</FILESIZE>')
            fileSize = int(firstPacketsAsString[fileSizeStart:fileSizeEnd])

            firstDataStart = firstPackets.index(bytes('</FILESIZE>', 'utf-8')) + len(bytes('</FILESIZE>', 'utf-8'))
            firstData = firstPackets[firstDataStart:]
            firstDataSize = len(firstData)

            with open('./' + file, "wb") as f:
                if firstDataSize > fileSize:
                    f.write(firstData[:fileSize])
                    firstPackets = firstData[fileSize:]
                    firstPacketsAsString = str(firstPackets, 'utf-8', errors='ignore')
                else:
                    remainingDataSize = fileSize - firstDataSize
                    f.write(firstData)
                    while remainingDataSize > 1024:
                        f.write(self.clientSocket.recv(1024))
                        remainingDataSize -= 1024
                    f.write(self.clientSocket.recv(remainingDataSize))
                    firstPackets = b''
                    firstPacketsAsString = ''

        self.disconnect()
        return True

    def getUpdate(self):
        """ Function to pull the newest client from the master.

                note:: Author(s): Mitch """
        from bfassist.standalone import KERN

        updateList = self.calculateDifferences()
        if updateList:
            installList = []
            for update in updateList:
                if update.endswith('.py'):
                    installList.append(update[:-3].replace('/', '.'))

            try:
                if self.getFiles(updateList):
                    KERN.AUTO_UPDATE_THREAD.toInstall += installList
                    return True
                else:
                    log("Couldn't receive update files correctly!", 3)
                    return False
            except timeout:
                log("Timeout while receiving update files.", 3)
                return False

#
#   # Server client_requests
#
#
#
