#############################################################################
#
#
#   RemoteConsole Module to BFA v.5 standalone
#
#
#############################################################################
""" This module handles interactions with the refractor remote console.

    Dependencies:

        bfassist <- (standalone.server.)remoteconsole
            |
            \-> bfa_logging
             -> standalone  @RemoteConsole.sendToConsole

        note::  Author(s): Mitch last-check: 08.07.2021 """

from os import name
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM

import struct

from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class RemoteConsole:
    """ Python implementation of a bf 1942 remote console interface.

        :param user:            Username for the RemoteConsole login.
        :param pw:              Password for the RemoteConsole login.
        :param ip:              (Non-localhost) Ip the RemoteConsole listens on.
        :param port:            Port the RemoteConsole listens on.

        :param rcSocket:         TCP-Socket for communicating with the RemoteConsole.
        :param authenticated:   Status flag for authentication with the server.

            note::  Author(s): Mitch """

    def __init__(self, user: str, pw: str, ip: str, port: str, authenticated: bool = False,
                 rcSocket: socket = socket(AF_INET, SOCK_STREAM)):
        self.user = user
        self.pw = pw
        self.ip = ip
        self.port = port
        self.authenticated = authenticated
        self.rcSocket = rcSocket

    def authenticate(self):
        """ Uses the supplied login information to authenticate with the server.

            :return: Returns True after successful authentication False otherwise.

                note::  Author(s): Mitch - loosely based on a script by Kees Cook """
        try:
            if not self.authenticated:

                data, addr = self.rcSocket.recvfrom(10)
                # Receiving xor challenge

                xor = struct.unpack("10c", data)
                # Unpacking challenge

                log('Received xor-Challenge pattern', 0)

                self.sendNum(len(self.user)+1)
                # Sending length of username

                response = struct.pack(str(len(self.user)+1)+"c", *XORencrypt(self.user, xor),
                                       int(0).to_bytes(1, 'little'))
                # Encoding and Encrypting username

                self.rcSocket.send(response)
                # Sending username cipher

                self.sendNum(len(self.pw)+1)
                # Sending length of password

                response = struct.pack(str(len(self.pw)+1) + "c", *XORencrypt(self.pw, xor),
                                       int(0).to_bytes(1, 'little'))
                # Encoding and Encrypting password

                self.rcSocket.send(response)
                # Sending password cipher

                data, addr = self.rcSocket.recvfrom(1)
                # Receive 1 byte

                if len(data) > 0 and data[0] == 1:
                    self.authenticated = True
                    return True
                else:
                    log('Authentication with RemoteConsole failed.', 3)
                    return False

            else:
                log('We were already authenticated!', 1)
                return True
        except ConnectionResetError:
            log("Receiver connection reset error. Waiting and trying again.", 3)
            sleep(5)
            self.renewSocket()
            return self.authenticate()

    def sendNum(self, inValue: int):
        """ Sends a numeric value packed with little-endian-order to the socket.

            :param inValue: Value to be sent.

                note::  Author(s): Mitch - loosely based on a script by Kees Cook """

        self.rcSocket.send(inValue.to_bytes(4, 'little'))

    def receiveNum(self):
        """ Receives 4 bytes treating it as a numerical value with little-endian-order.

            :return:    Returns the integer value of the first byte.

                note::  Author(s): Mitch - loosely based on a script by Kees Cook """

        data, addr = self.rcSocket.recvfrom(4)

        return int.from_bytes(data, 'little')

    def sendString(self, inValue: str):
        """ Sends a String by first transmitting length of the string + 1 then following up
            with the encoded string + a null-string byte at the end.

            :param inValue: String to be sent.

                note::  Author(s): Mitch - loosely based on a script by Kees Cook """

        self.sendNum(len(inValue) + 1)
        # sending length of string

        for c in inValue:
            if ord(c) > 255:
                print(c)

        self.rcSocket.send(struct.pack(str(len(inValue) + 1) + 'c',
                                       *[(ord(c) % 256).to_bytes(1, 'little') for c in inValue],
                                       int(0).to_bytes(1, 'little')))

    def receiveString(self):
        """ Receives a String from the server. When calling this function you should already
            be expecting an incoming string on the socket.

            :return: String that arrived on the socket.

                note::  Author(s): Mitch, henk - loosely based on a script by Kees Cook """

        strBytes = ""
        strLen = self.receiveNum()
        if name == 'nt':
            while strLen > 0:
                data = self.rcSocket.recv(strLen)
                strBytes += data.decode('ISO-8859-1')
                strLen -= 1400
            return strBytes
        else:
            data = self.rcSocket.recv(strLen)
            strBytes += data.decode('ISO-8859-1')
            return strBytes

    def sendToConsole(self, inCommand, count: int = 0):
        """ Sends a command to the RemoteConsole. Can only be used post-authentication.

            :param inCommand:   Command to be sent to the server. Optimally encoded with cp850 or ISO-8859-1.
            :param count:       Number of retries for sending the inCommand.

            :return:            Reply of the server if any. False if not authenticated.

                note::  Author(s): Mitch - loosely based on a script by Kees Cook """

        if not self.authenticated:
            from bfassist.standalone import KERN

            log("Trying to send command to console without prior authentication.", 2)
            if KERN.GLOBAL_MONITORING and count < 3:
                self.renewSocket()
                self.authenticate()
                count += 1
                return self.sendToConsole(inCommand, count)
            else:
                return False
        else:

            try:
                self.sendNum(2)
                self.sendString("ConsoleMessage 0")
                self.sendString(inCommand)

                if self.receiveNum() == 1:
                    return self.receiveString()

                else:
                    ret = self.receiveString()
                    log("Executing command at console failed! " + ret, 3)
                    return False

            except (BrokenPipeError, ConnectionRefusedError):
                self.authenticated = False
                self.rcSocket.close()
                if count < 3:
                    log("Pipe to Console was broken! Maybe the server changed map or shut down? Retrying Connection.",
                        3)
                    sleep(5)

                    try:
                        self.renewSocket()
                        self.authenticate()
                        return self.sendToConsole(inCommand, count + 1)

                    except ConnectionRefusedError:
                        self.authenticated = False
                        self.rcSocket.close()
                        if count < 3:
                            log("Pipe to Console was broken! "
                                "Maybe the server changed map or shut down? Retrying Connection.", 3)
                            sleep(5)

                            try:
                                self.renewSocket()
                                self.authenticate()
                                return self.sendToConsole(inCommand, count + 1)

                            except ConnectionRefusedError:
                                self.authenticated = False
                                self.rcSocket.close()
                                log("Pipe to Console was irrevocably broken. Giving up console communication.", 4)
                                return False

                        else:
                            log("Pipe to Console was irrevocably broken. Giving up console communication.", 4)
                            return False

                else:
                    log("Pipe to Console was irrevocably broken. Giving up console communication.", 4)
                    return False

    def getConsoleInfoBuffer(self):
        """ This works, however you have to constantly call it for it to provide any useful information.

            :return: Server-buffer as a string.

                note::  Author(s): Mitch """

        self.sendNum(2)
        self.sendString("ConsoleRun 0")
        self.sendNum(2)
        self.rcSocket.send(b'\x0d\x00')
        rec = self.rcSocket.recv(1400)
        return rec

    def connect(self, retries: int = 3):
        """ Function to connect the socket to the console cleanly.

                note::  Author(s): Mitch """

        try:
            self.rcSocket.connect((self.ip, int(self.port)))
        except (ConnectionRefusedError, OSError, TypeError):
            if retries > 0:
                log("Connection was refused by the Remote Console, trying again.", 3)
                self.renewSocket(retries-1)
            else:
                log("Connection was refused three consecutive times! Giving up...", 5)

    def disconnect(self):
        """ Function to disconnect from the console cleanly.

                note::  Author(s): Mitch """

        self.rcSocket.close()
        sleep(5)
        self.authenticated = False

    def renewSocket(self, retries: int = 3):
        """ Function to renew the console socket.

                note::  Author(s): Mitch """

        log("Renewing console socket.")
        self.disconnect()
        self.rcSocket = socket(AF_INET, SOCK_STREAM)
        self.rcSocket.settimeout(2)
        self.connect(retries)


def XORencrypt(clear, pattern):
    """ XOR-encrypts an input against a specified pattern.

        :param clear:   Input to be xor-ed.
        :param pattern: Pattern to be xor-ed against.

        :return: Encrypted input.

            note::  Author(s): Mitch - loosely based on a script by Kees Cook """
    i = 0
    cipher = []
    for c in clear:
        cipher.append((ord(c) ^ int.from_bytes(pattern[i], 'little')).to_bytes(1, 'little'))
        i = (i+1) % len(pattern)
    return cipher
