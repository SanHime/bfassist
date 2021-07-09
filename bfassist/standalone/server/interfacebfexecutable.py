#############################################################################
#
#
# Module of BFA introducing and managing the Server Bf Executable Interface Class
#
#
#############################################################################
""" This module manages the interface and interactions of the server objects with the references bfexecutable module.

    Dependencies:

        bfassist <- (standalone.)server <- interfacebffexecutable
            \
             -> references

        note::  Author(s): Mitch last-check: 08.07.2021 """

from os.path import exists

from bfassist.standalone.server import Server
from bfassist.references import createSafeReference, shaForFile, Binary, Binaries


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerExecutableInterface:
    """ The server executable interface lets a server object interact with its binary executable files.

        :param server:              The server this interface belongs to.
        :param pathToExecutables:   Path to the server executables for better readability.
        :param dynamicExecutable:   The dynamic executable Binary object.
        :param staticExecutable:    The static executable Binary object.

            note::Author(s): Mitch """

    def __init__(self, server: Server, pathToExecutables: str = None, dynamicExecutable: Binary = None,
                 staticExecutable: Binary = None):

        self.server = server

        if pathToExecutables:
            self.pathToExecutables = pathToExecutables
        else:
            self.pathToExecutables = self.server.getBFPath()

        self.dynamicExecutable = dynamicExecutable
        self.staticExecutable = staticExecutable

    def refreshBinary(self, binaryType: str):
        """ Function to refresh our knowledge of the installed binary of a particular type (static or dynamic).

            :param binaryType:  The type of the binary to refresh.

                note::  Author(s): Mitch """

        if exists(self.pathToExecutables + 'bf1942_lnxded.' + binaryType):
            digestOfExecutable = shaForFile(self.pathToExecutables + 'bf1942_lnxded.' + binaryType)
            knownExecutable = Binaries.fetchSingleWhere('Digest', digestOfExecutable)

            if knownExecutable:
                return knownExecutable
            else:
                createSafeReference(self.pathToExecutables + 'bf1942_lnxded.' + binaryType, 'binaries/original.dynamic')
                return Binary('original.' + binaryType, digestOfExecutable, 'bfassist/references/binaries/')

        else:
            log("Could not find the " + binaryType + " server executable.")
            return None

    def refreshBinaries(self):
        """ Function to refresh our knowledge of the installed binaries.

                note::  Author(s): Mitch """

        self.dynamicExecutable = self.refreshBinary('dynamic')
        self.staticExecutable = self.refreshBinary('static')

    def replaceBinaryPair(self, binaryKind: str):
        """ Function to replace the current binary pair with the one specified. Then sends exit to the console. This
        will hopefully make bfsmd restart the server.

            :param binaryKind:  The name of the binary pair.

            :return:            True if done correctly, False otherwise.

                todo::  When replacing bfsmd fully, relying on bfsmd to restart the server will not work anymore.
                note::  Author(s): Mitch """

        if binaryKind + ".dynamic" in Binaries and binaryKind + ".static" in Binaries:
            # todo:: self.writeToServer("Installing " + binaryKind + " binaries...")
            # todo:: self.writeToServer("Shutting server down to install binaries...")
            # todo:: self.writeToServer("This may take a while...")
            sleep(10)
            # todo:: execConsoleCommand("exit")
            sleep(1)
            binaries = Binaries[binaryKind + ".dynamic"], Binaries[binaryKind + ".static"]
            try:
                copyfile(binaries[0].getPath() + binaries[0].getName(),
                         self.pathToExecutables + 'bf1942_lnxded.dynamic')
                copyfile(binaries[1].getPath() + binaries[1].getName(),
                         self.pathToExecutables + 'bf1942_lnxded.static')
            except OSError:
                log("Replacing the binaries failed. Manual inspection required!", 4)
                return False
            self.dynamicExecutable = binaries[0]
            self.staticExecutable = binaries[1]
            return True
        else:
            self.writeToServer("Could not find " + binaryKind + " binaries.")
            log("Tried switching to binaries that were not present", 3)
            return False
