#############################################################################
#
#
#   Update/Upgrade Threading network Module to BFA c7
#
#
#############################################################################
""" This module handles networking from bfa 'client' to bfa 'master' and vice-versa. In particular it creates a thread
that should be able to automatically pull the latest version and if specified also upgrade to it.

    Dependencies:

        bfassist <- network <- updatethread
            \
             -> bfa_logging

        note::  Author(s): Mitch last-check: 09.07.2021 """

from time import sleep
from threading import Thread
from importlib import import_module, reload

from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class UpdateThread(Thread):
    """ Class that models a Thread that can automatically download the latest version available on the client if a new
    one is available.

        :param auto_upgrading:  Determines if the thread also installs the update after downloading it.
        :param update_interval: The interval in seconds in which the thread checks for updates.
        :param active:          Flag that indicates if the thread is supposed to continue to run or not.
        :param toInstall:       A list of modules that have been updated but not upgraded.
        :param getUpdate:       The update function that's to be called
        :param isClient:        Determines if this update thread is run by a client.

            note::  Author(s): Mitch """

    def __init__(self, auto_upgrading: bool = False, update_interval: int = 15, active: bool = False,
                 toInstall: list = None, getUpdate: callable = None, isClient: bool = True):
        super().__init__()
        self.auto_upgrading = auto_upgrading
        self.update_interval = update_interval
        self.active = active
        self.isClient = isClient
        if toInstall:
            self.toInstall = toInstall
        else:
            self.toInstall = []
        self.getUpdate = getUpdate

    def run(self):
        """ The functions that's run when the Thread is started. Contains the actual update-loop.

                note::  Author(s): Mitch """

        while self.active:
            if self.auto_upgrading:
                if self.getUpdate():
                    self.upgrade()
            sleep(self.update_interval)

    def upgrade(self):
        """ Function that upgrades everything specified in the install list.

                note::  Author(s): Mitch """

        while self.toInstall:
            self.upgradeModule(self.toInstall[0])

    def upgradeModule(self, modulePath: str):
        """ Function that imports a module and calls its reload function.

            :param modulePath:  Absolute module path.

                note::  Author(s): Mitch """

        log("Upgrading " + modulePath + ".")
        module = import_module(modulePath)
        module.__preload__(self.isClient)
        reload(module)
        module.__postload__(self.isClient)
        if modulePath in self.toInstall:
            self.toInstall.remove(modulePath)

    def start(self):
        """ Starts the thread and sets the active flag to True before.

                note::  Author(s): Mitch """

        self.active = True
        super().start()

    def stop(self):
        """ Stops the thread by setting the active flag to False.

                note::  Author(s): Mitch """

        self.active = False
        self.join()
