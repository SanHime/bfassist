#############################################################################
#
#
#   Version Control Module to BFA c7 Master
#
#
#############################################################################
""" This is the version control module for the bfa master.

    Dependencies:

        bfassist <- (master.)bfaversioncontrol
            |
            \-> bfa_logging
             -> network -> updatethread

        note::  Author(s): Mitch last-check: 08.07.2021 """

from svn.remote import RemoteClient
from importlib import reload
from sys import modules
from pathlib import Path

from bfassist.bfa_logging import log
from bfassist.network.updatethread import UpdateThread


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class MasterVersionControl:
    """ Class that will manage the bfa internal version control system of bfa for the master server.

        :param svnBaseURL:              Base location of the svn repository.
        :param activeStage:             Active stage.
        :param activeBranch:            Active branch.
        :param activeClientRevision:    The client revision that's currently available from the served client.
        :param svnClient:               Svn remote client on the active stage and branch.
        :param packageSignature:        Current package signature.

        :param AUTO_UPDATE_THREAD:      A Thread that can automatically update and if specified even upgrade at runtime.

            note::  Author(s): Mitch """

    def __init__(self, svnBaseURL: str, activeStage: str, activeBranch: str, activeClientRevision: str,
                 svnClient: RemoteClient = None, packageSignature: dict = None,
                 AUTO_UPDATE_THREAD: UpdateThread = None):

        self.svnBaseURL = svnBaseURL
        self.activeStage = activeStage
        self.activeBranch = activeBranch
        self.activeClientRevision = activeClientRevision
        if packageSignature:
            self.packageSignature = packageSignature
        else:
            self.packageSignature = self.createPackageSignature()

        if svnClient:
            self.svnClient = svnClient
        else:
            self.svnClient = RemoteClient(self.svnBaseURL + self.activeStage + self.activeBranch)

        if AUTO_UPDATE_THREAD:
            self.AUTO_UPDATE_THREAD = AUTO_UPDATE_THREAD
        else:
            self.AUTO_UPDATE_THREAD = UpdateThread(getUpdate=self.pullLatestRevisionFromBranch, isClient=False)

    @staticmethod
    def createPackageSignature():
        """ Functions that's similar to the folder signature creation of the master baserequesthandler. However, this
        function only considers python modules, so files that end with '.py'.

            :return:    Dictionary containing the package signature of the entire c7 branch.

                note::  Author(s): Mitch """

        from bfassist.references import shaForFile

        signature = {}
        for cPath in Path('.').glob('**/*'):
            if not cPath.is_dir() and str(cPath).endswith('.py'):
                signature[str(cPath)] = shaForFile(str(cPath))
        return signature

    def updateSignature(self, new: dict):
        """ Function to compare two package signatures.

            :param new: The new package signature.

                note::  Author(s): Mitch """

        differences = []
        for file in new:
            if file in self.packageSignature and new[file] == self.packageSignature[file]:
                pass
            else:
                differences += new[file][:-3].replace('/', '.')

        if differences:
            self.packageSignature = new
        return differences

    def pullLatestRevisionFromBranch(self):
        """ Function to pull the latest revision of this branch from svn. This will include the files for the client
        that can be downloaded from the master.

                note:: Author(s): Mitch """

        self.svnClient.export('.', force=True)
        possibleChange = self.createPackageSignature()
        self.AUTO_UPDATE_THREAD.toInstall += self.updateSignature(possibleChange)

        self.activeClientRevision = str(self.svnClient.info()['commit_revision'])
        self.injectVersionInformation()

    def injectVersionInformation(self):
        """ Function to inject the version information into the bfa files that is the current active client revision.
        Stage and branch changes can only be done manually thus far.

                note::  Author(s): Mitch """

        if self.activeStage == "development/":
            varLine = "DEVELOPMENT_ACTIVE_CLIENT_REVISION = None\n"
            re = "DEVELOPMENT_ACTIVE_CLIENT_REVISION = "
        elif self.activeStage == "experimental/":
            varLine = "EXPERIMENTAL_ACTIVE_CLIENT_REVISION = None\n"
            re = "EXPERIMENTAL_ACTIVE_CLIENT_REVISION = "
        else:
            varLine = None
            re = None

        with open("bfassist/master/__init__.py", 'r+') as masterVersionFile:
            output = ""
            for line in masterVersionFile:
                if line == varLine:
                    output += re + "\"" + self.activeClientRevision + "\"\n"
                else:
                    output += line
            masterVersionFile.seek(0)
            masterVersionFile.write(output)
            masterVersionFile.truncate()

        with open("bfassist/network/config.ini", 'r+') as networkConfigFile:
            output = ""
            for line in networkConfigFile:
                if line == 'revision = ""':
                    output += 'revision = "' + self.activeClientRevision + '"\n'
                else:
                    output += line
            networkConfigFile.seek(0)
            networkConfigFile.write(output)
            networkConfigFile.truncate()

    def upgrade(self):
        """ Function to do manual upgrades when auto-upgrades are off.

                note::  Author(s): Mitch """

        self.AUTO_UPDATE_THREAD.upgrade()
