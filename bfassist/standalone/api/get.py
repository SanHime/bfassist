#############################################################################
#
#
#   API GET requests that are served by BF-A mainly for the webservice
#
#
#############################################################################
""" API for BF-A: GET requests.

    Dependencies:

        bfassist <- standalone <- (api.)get
            |
            |-> api
            |-> usersystem
            \-> standalone -> admin -> administrationcore
             -> network

        note::  Author(s): Mitch last-check: 08.07.2021 """

import json

from bfassist.api import api_GET

from bfassist.standalone import BFAKern, Player, Players, Server
from bfassist.usersystem import BFAUser, BFAUsers, BFARight
from bfassist.standalone.admin.administrationcore import ServerAdministrationCore
from bfassist.network import BFA_Settings


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class api_GETs:
    """ The class that connects the kern and the api get requests.

            note::  Author(s): Mitch """

    KERN = None

    def __init__(self, KERN: BFAKern):
        api_GETs.KERN = KERN

    @staticmethod
    def getBFAUser(Keyhash: str) -> BFAUser.typeHint(): return BFAUsers[Keyhash].toLocalDict()

    @staticmethod
    def getBFAUsers() -> [BFAUser.typeHint()]: return [user.toLocalDict() for user in BFAUsers.liveSet]

    @staticmethod
    def getBFARightScheme() -> BFARight.typeHintBFARights(): return BFARight.BFARights

    @staticmethod
    def getPlayer(Keyhash: str) -> Player.typeHint(): return Players[Keyhash].toGlobalDict()

    @staticmethod
    def getGlobalMonitoring() -> bool: return api_GETs.KERN.GLOBAL_MONITORING

    @staticmethod
    def getServer(BFAName: str) -> Server.typeHint(): return api_GETs.KERN.REGISTERED_SERVERS[BFAName].toLocalDict()

    @staticmethod
    def getServers() -> [Server.typeHint()]:
        return [SERVER.toLocalDict() for SERVER in api_GETs.KERN.REGISTERED_SERVERS]

    @staticmethod
    def getUpdate() -> list: return list(api_GETs.KERN.BFA_NETWORK.calculateDifferences())

    @staticmethod
    def getAutoUpdateSetting() -> bool: return api_GETs.KERN.CONFIG[BFA_Settings]['auto-update']

    @staticmethod
    def getAutoUpgradeSetting() -> bool: return api_GETs.KERN.CONFIG[BFA_Settings]['auto-upgrade']

    @staticmethod
    def getLeagueExtensionAvailability() -> bool: return api_GETs.KERN.CONFIG[BFA_Settings]['league-extensions']

    @staticmethod
    def getInGameCommands(BFAName: str) -> ServerAdministrationCore.typeHintInGameCommands():
        return api_GETs.KERN.REGISTERED_SERVERS[BFAName].InGameAdministration.listInGameCommands()


for attribute in dir(api_GETs):
    attr = getattr(api_GETs, attribute)
    if callable(attr):
        if not attribute.startswith('__'):
            api_GET(attr)
