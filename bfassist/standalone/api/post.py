#############################################################################
#
#
#   API POST requests that are served by BF-A mainly for the webservice
#
#
#############################################################################
""" API for BF-A: POST requests.

    Dependencies:

        bfassist <- standalone <- (api.)post
            |
            |-> api
            \-> standalone
             -> usersystem

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.api import api_POST

from bfassist.standalone import BFAKern, Player, Server
from bfassist.usersystem import BFAUser, BFAUsers


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class api_POSTs:
    """ The class that connects the kern and the api post requests.

            note::  Author(s): Mitch """

    KERN = None

    def __init__(self, KERN: BFAKern):
        api_POSTs.KERN = KERN

    @staticmethod
    def createBFAUser(Keyhash: str) -> BFAUser.typeHint(): return BFAUser(Keyhash).toLocalDict()

    @staticmethod
    def deleteBFAUser(Keyhash: str) -> bool: return BFAUsers[Keyhash].delete()

    @staticmethod
    def createServer(BFAName: str, BFPath: str) -> Server.typeHint(): return Server(BFAName, BFPath).toLocalDict()

    @staticmethod
    def deleteServer(BFAName: str) -> bool: return api_POSTs.KERN.REGISTERED_SERVERS[BFAName].delete()

    @staticmethod
    def addPlayer(Keyhash: str, Alias: str) -> Player.typeHint(): return Player(Keyhash, Alias).toGlobalDict()

    @staticmethod
    def executeConsoleCommand(BFAName: str, command: str) -> str: return\
        str(api_POSTs.KERN.REGISTERED_SERVERS[BFAName].ConsoleInterface.executeConsoleCommand(command))

    @staticmethod
    def writeToServer(BFAName: str, inMessage: str) -> bool: return\
        api_POSTs.KERN.REGISTERED_SERVERS[BFAName].ConsoleInterface.writeToServer(inMessage)

    @staticmethod
    def bfaUpdate() -> None: return\
        api_POSTs.KERN.BFA_NETWORK.getUpdate()

    @staticmethod
    def bfaUpgrade() -> None: return\
        api_POSTs.KERN.upgrade()


for attribute in dir(api_POSTs):
    attr = getattr(api_POSTs, attribute)
    if callable(attr):
        if not attribute.startswith('__'):
            api_POST(attr)
