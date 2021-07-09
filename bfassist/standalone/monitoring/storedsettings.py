#############################################################################
#
#
# Module of BFA that is in charge of storing server settings information
#
#
#############################################################################
""" This module implements the logging and storing of Bf-Round Settings.

    Dependencies:

        bfassist <- (standalone.monitoring.)storedsettings
            \
             -> sql

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BfServerSetting(DBStorable, table="settings", live=False):
    """ A BfServerSetting is supposed to correspond to the server settings on a server at the start of a particular
    round.

        :param SettingsId:          Identifier of this particular settings.
        :param ServerName:          Name of the server.
        :param GamePort:            Game port.
        :param Dedicated:           Is dedicated.
        :param ModId:               Mod id.
        :param MapId:               Map id.
        :param Map:                 Map.
        :param GameMode:            Game mode.
        :param GameTime:            Round time limit.
        :param MaxPlayers:          Maximum number of livePlayers.
        :param ScoreLimit:          Score limit.
        :param NoRounds:            Number of rounds.
        :param SpawnTime:           Spawn time.
        :param SpawnDelay:          Spawn delay.
        :param GameStartDelay:      Game start delay.
        :param RoundStartDelay:     Round start delay.
        :param SoldierFf:           Soldier friendly fire.
        :param VehicleFf:           Vehicle friendly fire.
        :param TicketRatio:         Ticket ratio.
        :param Internet:            Internet server.
        :param AlliedTr:            Allied tr.
        :param AxisTr:              Axis tr.
        :param CoopSkill:           AI skill.
        :param CoopCpu:             CPU % reserved for ai.
        :param ReservedSlots:       Number of reserved slots.
        :param AllowNoseCam:        Allow nose camera mode.
        :param FreeCamera:          Free camera mode.
        :param ExternalViews:       External views mode.
        :param AutoBalance:         Auto balancing mode.
        :param TagDistance:         Tag visibility distance.
        :param TagDistanceScope:    Tag visibility distance when scoped.
        :param KickBack:            Kick back of friendly fire damage.
        :param KickBackSplash:      Kick back of friendly fire splash damage.
        :param SoldierFfOnSplash:   Soldier friendly fire on splash.
        :param VehicleFfOnSplash:   Vehicle friendly fire on splash.
        :param HitIndication:       Hit indication.
        :param TkPunish:            Team kill punish mode.
        :param CrossHairPoint:      Cross hair point.
        :param DeathCamType:        Type of the death cam.
        :param ContentCheck:        Content check mode.
        :param Sv_Punkbuster:       Punkbuster.

            note::  Author(s): Mitch """

    def __init__(self, ServerName: str = None, GamePort: int = None, Dedicated: int = None, ModId: str = None,
                 MapId: str = None, Map: str = None, GameMode: str = None, GameTime: int = None, MaxPlayers: int = None,
                 ScoreLimit: int = None, NoRounds: int = None, SpawnTime: int = None, SpawnDelay: int = None,
                 GameStartDelay: int = None, RoundStartDelay: int = None, SoldierFf: int = None, VehicleFf: int = None,
                 TicketRatio: int = None, Internet: int = None, AlliedTr: int = None, AxisTr: int = None,
                 CoopSkill: int = None, CoopCpu: int = None, ReservedSlots: int = None, AllowNoseCam: int = None,
                 FreeCamera: int = None, ExternalViews: int = None, AutoBalance: int = None, TagDistance: int = None,
                 TagDistanceScope: int = None, KickBack: int = None, KickBackSplash: int = None,
                 SoldierFfOnSplash: int = None, VehicleFfOnSplash: int = None, HitIndication: int = None,
                 TkPunish: int = None, CrossHairPoint: int = None, DeathCamType: int = None, ContentCheck: int = None,
                 Sv_Punkbuster: int = None, SettingsId: int = None):

        self.SSettingsId = SettingsId, INTEGER, PRIMARY_KEY
        self.SServerName = ServerName, VARCHAR(32)
        self.SGamePort = GamePort, MEDIUMINT
        self.SDedicated = Dedicated, BIT
        self.SModId = ModId, VARCHAR(32)
        self.SMapId = MapId, VARCHAR(32)
        self.SMap = Map, VARCHAR(64)
        self.SGameMode = GameMode, VARCHAR(32)
        self.SGameTime = GameTime, TINYINT
        self.SMaxPlayers = MaxPlayers, SMALLINT
        self.SScoreLimit = ScoreLimit, SMALLINT
        self.SNoRounds = NoRounds, TINYINT
        self.SSpawnTime = SpawnTime, TINYINT
        self.SSpawnDelay = SpawnDelay, TINYINT
        self.SGameStartDelay = GameStartDelay, TINYINT
        self.SRoundStartDelay = RoundStartDelay, TINYINT
        self.SSoldierFf = SoldierFf, TINYINT
        self.SVehicleFf = VehicleFf, TINYINT
        self.STicketRatio = TicketRatio, TINYINT
        self.SInternet = Internet, BIT
        self.SAlliedTr = AlliedTr, BIT
        self.SAxisTr = AxisTr, BIT
        self.SCoopSkill = CoopSkill, TINYINT
        self.SCoopCpu = CoopCpu, TINYINT
        self.SReservedSlots = ReservedSlots, TINYINT
        self.SAllowNoseCam = AllowNoseCam, BIT
        self.SFreeCamera = FreeCamera, BIT
        self.SExternalViews = ExternalViews, BIT
        self.SAutoBalance = AutoBalance, BIT
        self.STagDistance = TagDistance, SMALLINT
        self.STagDistanceScope = TagDistanceScope, SMALLINT
        self.SKickBack = KickBack, TINYINT
        self.SKickBackSplash = KickBackSplash, TINYINT
        self.SSoldierFfOnSplash = SoldierFfOnSplash, TINYINT
        self.SVehicleFfOnSplash = VehicleFfOnSplash, TINYINT
        self.SHitIndication = HitIndication, BIT
        self.STkPunish = TkPunish, BIT
        self.SCrossHairPoint = CrossHairPoint, BIT
        self.SDeathCamType = DeathCamType, BIT
        self.SContentCheck = ContentCheck, BIT
        self.SSv_Punkbuster = Sv_Punkbuster, BIT

        self.insertToDB()

    @staticmethod
    def typeHint():
        return {
            'ServerName': str,
            'GamePort': int,
            'Dedicated': int,
            'ModId': int,
            'MapId': str,
            'Map': str,
            'GameMode': str,
            'GameTime': int,
            'MaxPlayers': int,
            'ScoreLimit': int,
            'NoRounds': int,
            'SpawnTime': int,
            'SpawnDelay': int,
            'GameStartDelay': int,
            'RoundStartDelay': int,
            'SoldierFf': int,
            'VehicleFf': int,
            'TicketRatio': int,
            'Internet': int,
            'AlliedTr': int,
            'AxisTr': int,
            'CoopSkill': int,
            'CoopCpu': int,
            'ReservedSlots': int,
            'AllowNoseCam': int,
            'FreeCamera': int,
            'ExternalViews': int,
            'AutoBalance': int,
            'TagDistance': int,
            'TagDistanceScope': int,
            'KickBack': int,
            'KickBackSplash': int,
            'SoldierFfOnSplash': int,
            'VehicleFfOnSplash': int,
            'HitIndication': int,
            'TkPunish': int,
            'CrossHairPoint': int,
            'DeathCamType': int,
            'ContentCheck': int,
            'Sv_Punkbuster': int
        }

    def toGlobalDict(self):
        """ Function to convert server settings into a dictionary for the global bfa perspective and make it json
        serializable.

            :return:    The settings as dictionary.

                note::  Author(s): Mitch """

        return {
            'ServerName':           self.getServerName(),
            'GamePort':             self.getGamePort(),
            'Dedicated':            self.getDedicated(),
            'ModId':                self.getModId(),
            'MapId':                self.getMapId(),
            'Map':                  self.getMap(),
            'GameMode':             self.getGameMode(),
            'GameTime':             self.getGameTime(),
            'MaxPlayers':           self.getMaxPlayers(),
            'ScoreLimit':           self.getScoreLimit(),
            'NoRounds':             self.getNoRounds(),
            'SpawnTime':            self.getSpawnTime(),
            'SpawnDelay':           self.getSpawnDelay(),
            'GameStartDelay':       self.getGameStartDelay(),
            'RoundStartDelay':      self.getRoundStartDelay(),
            'SoldierFf':            self.getSoldierFf(),
            'VehicleFf':            self.getVehicleFf(),
            'TicketRatio':          self.getTicketRatio(),
            'Internet':             self.getInternet(),
            'AlliedTr':             self.getAlliedTr(),
            'AxisTr':               self.getAxisTr(),
            'CoopSkill':            self.getCoopSkill(),
            'CoopCpu':              self.getCoopCpu(),
            'ReservedSlots':        self.getReservedSlots(),
            'AllowNoseCam':         self.getAllowNoseCam(),
            'FreeCamera':           self.getFreeCamera(),
            'ExternalViews':        self.getExternalViews(),
            'AutoBalance':          self.getAutoBalance(),
            'TagDistance':          self.getTagDistance(),
            'TagDistanceScope':     self.getTagDistanceScope(),
            'KickBack':             self.getKickBack(),
            'KickBackSplash':       self.getKickBackSplash(),
            'SoldierFfOnSplash':    self.getSoldierFfOnSplash(),
            'VehicleFfOnSplash':    self.getVehicleFfOnSplash(),
            'HitIndication':        self.getHitIndication(),
            'TkPunish':             self.getTkPunish(),
            'CrossHairPoint':       self.getCrossHairPoint(),
            'DeathCamType':         self.getDeathCamType(),
            'ContentCheck':         self.getContentCheck(),
            'Sv_Punkbuster':        self.getSv_Punkbuster()
        }

    def check(self, toCompare: dict):
        """ Function to compare settings with those specified in a dictionary to see if they match.

            :param toCompare:   A settings dictionary that will be matched against.

            :return:            A dictionary containing all mismatches.

                note::  Author(s): Mitch """

        for setting in set(toCompare.keys()):
            if toCompare[setting] == self.__getattribute__('get' + setting)():
                toCompare.pop(setting)
            else:
                toCompare[setting] = toCompare[setting], self.__getattribute__('get' + setting)()

        return toCompare


BfServerSettings = BfServerSetting.storageDict
