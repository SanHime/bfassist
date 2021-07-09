#############################################################################
#
#
#   API PUT requests that are served by BF-A mainly for the webservice
#
#
#############################################################################
""" API for BF-A: PUT requests.

    Dependencies:

        bfassist <- standalone <- (api.)put
            |
            |-> api
            \-> standalone
             -> usersystem

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.api import api_PUT

from bfassist.standalone import BFAKern
from bfassist.usersystem import BFAUsers, BFAUser, BFARight


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class api_PUTs:
    """ The class that connects the kern and the api put requests.

            note::  Author(s): Mitch """

    KERN = None

    def __init__(self, KERN: BFAKern):
        api_PUTs.KERN = KERN

    @staticmethod
    def connectWithServer(BFAName: str) -> bool: return \
        api_PUTs.KERN.REGISTERED_SERVERS[BFAName].MonitoringInterface.connect()

    @staticmethod
    def disconnectFromServer(BFAName: str) -> bool: return \
        api_PUTs.KERN.REGISTERED_SERVERS[BFAName].MonitoringInterface.disconnect()

    @staticmethod
    def stop() -> bool: return api_PUTs.KERN.stop()

    @staticmethod
    def start() -> bool: return api_PUTs.KERN.start()

    # The following 3 functions are "fake" and meant to "shadow" the login, logout and registration of the webservice
    @staticmethod
    def loginBFAUser(Keyhash: str, User: str, Pass: str) -> bool: pass
    """ bfaUser = BFAUsers[Keyhash]
        if bfaUser.credentialsMatch(User, Pass):
            if bfaUser.allowsMultipleLogins() or not bfaUser.isOnline():
                bfaUser.login() """

    @staticmethod
    def logoutBFAUser() -> bool: pass

    @staticmethod
    def registerBFAUser(Keyhash: str, User: str, Pass: str) -> bool: pass
    """ BFAUsers[Keyhash].setUser(User)
        BFAUsers[Keyhash].setPass(Pass) """

    @staticmethod
    def editBFAUser(Keyhash: str, newKeyhash: str, newRights: str, newMultiLogin: str) -> bool:
        return BFAUsers[Keyhash].editUser(newKeyhash, newRights, newMultiLogin)

    @staticmethod
    def editServer(BFAName: str, newBFAName: str, newBFPath: str) -> bool:
        return api_PUTs.KERN.REGISTERED_SERVERS[BFAName].editServer(newBFPath, newBFAName)

    @staticmethod
    def toggleAutoUpdateSetting() -> bool: return api_PUTs.KERN.toggleAutoUpdate()

    @staticmethod
    def toggleAutoUpgradeSetting() -> bool: return api_PUTs.KERN.toggleAutoUpgrade()


for attribute in dir(api_PUTs):
    attr = getattr(api_PUTs, attribute)
    if callable(attr):
        if not attribute.startswith('__'):
            api_PUT(attr)
