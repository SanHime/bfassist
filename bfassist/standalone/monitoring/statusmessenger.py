#############################################################################
#
#
# Module of BFA that sends status messages to the server
#
#
#############################################################################
""" This module implements thread-utilization for status messaging.

    Dependencies:

        bfassist <- (standalone.monitoring.)statusmessenger
            |
            \-> bfa_logging
             -> standalone

        note::  Author(s): Mitch last-check: 08.07.2021 """

from threading import Thread
from time import sleep

from bfassist.bfa_logging import log
from bfassist.standalone import Server


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class StatusMessenger(Thread):
    """ Thread for sending Status-Messages to the Server.

        :param server:              Server Object the Status-Messenger attaches to.
        :param message_interval:    Duration in seconds between two status messages.
        :param longest_sleep:       Longest time in seconds that the thread is allowed to sleep without checking its
                                    run-condition.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, message_interval: int = 90, longest_sleep: int = 5):

        Thread.__init__(self)
        self.server = server
        self.message_interval = message_interval
        self.longest_sleep = longest_sleep

    def run(self):

        log("Starting the status Messenger for a server.", 1)
        self.server.ConsoleInterface.writeToServer('Hello everyone, connecting to BFA now')
        while self.server.monitoringIsActive():
            try:
                self.server.ConsoleInterface.writeToServer('This server is connected with BFA')
            except RuntimeError:
                pass
            finally:
                for x in range(self.message_interval//self.longest_sleep):
                    if self.server.monitoringIsActive():
                        sleep(self.longest_sleep)
                    else:
                        break
        log("Stopping the status Messenger for a server.", 1)
