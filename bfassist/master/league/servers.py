#############################################################################
#
#
# Module of BFA that manages league activity concerning players
#
#
#############################################################################
""" This module should introduce functionality related to league activity. Especially such that is closely related to
servers.

    Dependencies:

        bfassist <- (master.league.)servers
            \
             -> sql


        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


LEAGUE_SETTINGS = {
    'ModId':                'bf1942',
    'MapId':                'BF1942',
    'GameMode':             'GPM_CQ',
    'GameTime':             20,
    'MaxPlayers':           32,
    'ScoreLimit':           0,
    'SpawnTime':            20,
    'SpawnDelay':           3,
    'GameStartDelay':       20,
    'RoundStartDelay':      10,
    'SoldierFf':            100,
    'VehicleFf':            100,
    'AlliedTr':             1,
    'AxisTr':               1,
    'ReservedSlots':        0,
    'AllowNoseCam':         1,
    'FreeCamera':           0,
    'ExternalViews':        1,
    'AutoBalance':          0,
    'TagDistance':          100,
    'TagDistanceScope':     300,
    'KickBack':             0,
    'KickBackSplash':       0,
    'SoldierFfOnSplash':    100,
    'VehicleFfOnSplash':    100,
    'HitIndication':        1,
    'TkPunish':             1,
    'CrossHairPoint':       1,
    'DeathCamType':         0,
    'ContentCheck':         0,
    'Sv_Punkbuster':        1
}


class BfServerSetting(DBStorable, table="bfserversettings", live=False):
    """ A bf server setting is supposed to correspond to the global bfa perspective of a server setting managed by a bfa
     client.

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

    def __init__(self, ServerName: str, GamePort: int, Dedicated: int, ModId: str, MapId: str, Map: str, GameMode: str,
                 GameTime: int, MaxPlayers: int, ScoreLimit: int, NoRounds: int, SpawnTime: int, SpawnDelay: int,
                 GameStartDelay: int, RoundStartDelay: int, SoldierFf: int, VehicleFf: int, TicketRatio: int,
                 Internet: int, AlliedTr: int, AxisTr: int, CoopSkill: int, CoopCpu: int, ReservedSlots: int,
                 AllowNoseCam: int, FreeCamera: int, ExternalViews: int, AutoBalance: int, TagDistance: int,
                 TagDistanceScope: int, KickBack: int, KickBackSplash: int, SoldierFfOnSplash: int,
                 VehicleFfOnSplash: int, HitIndication: int, TkPunish: int, CrossHairPoint: int, DeathCamType: int,
                 ContentCheck: int, Sv_Punkbuster: int, SettingsId: int = None):

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

    @classmethod
    def fromDict(cls, settingsDict: dict):
        if settingsDict:
            return cls(ServerName=settingsDict['ServerName'], GamePort=settingsDict['GamePort'],
                       Dedicated=settingsDict['Dedicated'], ModId=settingsDict['ModId'], MapId=settingsDict['MapId'],
                       Map=settingsDict['Map'], GameMode=settingsDict['GameMode'], GameTime=settingsDict['GameTime'],
                       MaxPlayers=settingsDict['MaxPlayers'], ScoreLimit=settingsDict['ScoreLimit'],
                       NoRounds=settingsDict['NoRounds'], SpawnTime=settingsDict['SpawnTime'],
                       SpawnDelay=settingsDict['SpawnDelay'], GameStartDelay=settingsDict['GameStartDelay'],
                       RoundStartDelay=settingsDict['RoundStartDelay'], SoldierFf=settingsDict['SoldierFf'],
                       VehicleFf=settingsDict['VehicleFf'], TicketRatio=settingsDict['TicketRatio'],
                       Internet=settingsDict['Internet'], AlliedTr=settingsDict['AlliedTr'],
                       AxisTr=settingsDict['AxisTr'], CoopSkill=settingsDict['CoopSkill'],
                       CoopCpu=settingsDict['CoopCpu'], ReservedSlots=settingsDict['ReservedSlots'],
                       AllowNoseCam=settingsDict['AllowNoseCam'], FreeCamera=settingsDict['FreeCamera'],
                       ExternalViews=settingsDict['ExternalViews'], AutoBalance=settingsDict['AutoBalance'],
                       TagDistance=settingsDict['TagDistance'], TagDistanceScope=settingsDict['TagDistanceScope'],
                       KickBack=settingsDict['KickBack'], KickBackSplash=settingsDict['KickBackSplash'],
                       SoldierFfOnSplash=settingsDict['SoldierFfOnSplash'],
                       VehicleFfOnSplash=settingsDict['VehicleFfOnSplash'], HitIndication=settingsDict['HitIndication'],
                       TkPunish=settingsDict['TkPunish'], CrossHairPoint=settingsDict['CrossHairPoint'],
                       DeathCamType=settingsDict['DeathCamType'], ContentCheck=settingsDict['ContentCheck'],
                       Sv_Punkbuster=settingsDict['Sv_Punkbuster'])
        else:
            return cls(*(None,) * 41)


ServerSettings = BfServerSetting.storageDict


class BfServerBinary(DBStorable, table="bfserverbinaries", live=False):
    """ A bf server binary is supposed to correspond to the global bfa perspective of a server binary managed by a bfa
     client.

        :param Name:    Name of the Binary.
        :param Digest:  SHA-256 hex-digest of this binary.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, Digest: str):

        self.SDigest = Digest, TEXT, PRIMARY_KEY
        self.SName = Name, VARCHAR(255)

        self.insertToDB()

    @classmethod
    def fromDict(cls, binaryDict: dict):
        if binaryDict:
            return cls(Name=binaryDict['Name'], Digest=binaryDict['Digest'])
        else:
            return cls(*(None,) * 2)


ServerBinaries = BfServerBinary.storageDict


class BfServer(DBStorable, table="bfservers", live=False):
    """ A bf server is supposed to correspond to the global bfa perspective of a bf server managed by a bfa client.

        :param binaries:        A global bfa server binary representation.
        :param hasHenkPatch:    A dictionary containing the different types of henk patches and their boolean flags if
                                the respective patch is enabled.

        :param Address:         The address of the server consisting of ip:port.
        :param BFAName:         The bfa name of the server.
        :param BinaryDigest:    Identifier for the corresponding binary that was last knowingly used.
        :param LocalUP:         Flag that signifies the bfa monitoring state of a server.


            note::  Author(s): Mitch """

    def __init__(self, Address: str, BFAName: str, LocalUP: int, BinaryDigest: str = None, binaries: dict = None,
                 hasHenkPatch: dict = None):

        if binaries and binaries['Digest'] in ServerBinaries:
            print("Binary exists already")
            self.binaries = ServerBinaries[binaries['Digest']]
            if binaries['Name'] != self.binaries.getName():
                self.binaries.setName(binaries['Name'])
        else:
            self.binaries = BfServerBinary.fromDict(binaries)
        self.hasHenkPatch = hasHenkPatch

        self.SAddress = Address, VARCHAR(255), PRIMARY_KEY
        self.SBFAName = BFAName, VARCHAR(255)
        if BinaryDigest:
            self.SBinaryDigest = BinaryDigest, TEXT
        else:
            self.SBinaryDigest = self.binaries.getDigest(), TEXT
        self.SLocalUP = LocalUP, BIT

        self.insertToDB()

    @classmethod
    def fromDict(cls, serverDict: dict):
        if serverDict:
            return cls(Address=serverDict['ip'] + ':' + serverDict['gamePort'], BFAName=serverDict['BFAName'],
                       binaries=serverDict['dynamicExecutable'], LocalUP=int(serverDict['local_monitoring']),
                       hasHenkPatch=serverDict['hasHenkPatch'])
        else:
            return cls(*(None,) * 4)


LeagueServers = BfServer.storageDict
