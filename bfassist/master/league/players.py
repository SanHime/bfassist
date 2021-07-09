#############################################################################
#
#
# Module of BFA that manages league activity concerning players
#
#
#############################################################################
""" This module should introduce functionality related to league activity. Especially such that is closely related to
players.

    Dependencies:

        bfassist <- (master.league.)players
            |
            \-> sql
             -> league @LeaguePlayer.setRegistration, @LeaguePlayer.fromDict

        note::  Author(s): Mitch last-check: 07.07.2021 """


from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class LeaguePlayer(DBStorable, table='players', live=False):
    """ Modelling a participant of the league.

        :param Keyhash:     Keyhash of the player.
        :param Alias:       Alias of the player.
        :param Aliases:     Set of other aliases.
        :param Ips:         Set of ips that were traced for this player.

        :param Team:        League team name of the player.
        :param Nomination:  League team name the player nominates.

            note::  Author(s): Mitch """

    def __init__(self, Keyhash: str, Alias: str, Aliases: set, Ips: set,

                 Team: str = "", Nomination: str = ""):
        self.SKeyhash = Keyhash, VARCHAR(32), PRIMARY_KEY
        self.SAlias = Alias, VARCHAR(32)
        self.SAliases = Aliases, MEDIUMTEXT
        self.SIps = Ips, TEXT
        self.STeam = Team, VARCHAR(32)
        self.SNomination = Nomination, VARCHAR(32)

        self.insertToDB()

    def addAlias(self, inAlias: str):
        """ Function to add an alias to the set of aliases(including database update).

            :param inAlias: The alias to add to the set of aliases of the player.

                note::  Author(s) : Mitch """

        self.getAliases().add(inAlias)
        try:
            self.__class__.storageDict.dbLock.acquire(True)
            self.__class__.storageDict.db.execute("UPDATE players SET Aliases=? WHERE Keyhash=?",
                                                  (";".join([x.replace(';', '\\&r01') for x in self.getAliases()]),
                                                   self.getKeyhash(),))
            self.__class__.storageDict.bfaSQLdatabase.commit()
        finally:
            self.__class__.storageDict.dbLock.release()

    def addIp(self, inIp: str):
        """ Function to add an ip to the set of ips(including database update).

            :param inIp: The ip to add to the set of ips of the player.

                note::  Author(s) : Mitch """

        self.getIps().add(inIp)
        try:
            self.__class__.storageDict.dbLock.acquire(True)
            self.__class__.storageDict.db.execute("UPDATE players SET Ips=? WHERE Keyhash=?",
                                                  (";".join(self.getIps()), self.getKeyhash(),))
            self.__class__.storageDict.bfaSQLdatabase.commit()
        finally:
            self.__class__.storageDict.dbLock.release()

    def __str__(self):
        return self.toString()

    def toString(self):
        """ Function to turn a player into an easily readable string. Mainly for debugging purposes.

                note::  Author(s): Mitch """

        return "Keyhash: " + self.getKeyhash() + ", Alias: " + self.getAlias() + ", Aliases: " + str(self.getAliases())\
               + ", Ips: " + str(self.getIps()) + ", Team: " + self.getTeam() + ", Nomination: " + self.getNomination()

    def setRegistration(self, team: str):
        """ Function to register a livePlayers team.

            :param team:    The team this player should be registered for.

            :return:        True if the player could be registered for this team, False otherwise.

                note::  Author(s): Mitch """

        from bfassist.master.league import CURRENT_SEASON

        if team in CURRENT_SEASON.getNominations():
            self.setTeam(team)
            return True
        else:
            return False

    def isLeader(self):
        """ Function to check if this player is a leader of any league team.

            :return:    True if the player is a leader otherwise false.

                note::  Author(s): Mitch """

        if any([True if team.getTeamLeader().getKeyhash() == self.getKeyhash() else False for team in LeagueTeams]):
            return True
        else:
            return False

    @classmethod
    def fromDict(cls, playerDict: dict):
        from bfassist.master.league import CURRENT_SEASON

        if 'nomination' in playerDict:
            nomination = playerDict['nomination']
        else:
            nomination = ""

        if 'registration' in playerDict and playerDict['registration'] in CURRENT_SEASON.getNominations():
            registration = playerDict['registration']
        else:
            registration = ""

        return cls(Keyhash=playerDict['Keyhash'], Alias=playerDict['Alias'],
                   Aliases=playerDict['Aliases'].replace('{', '').replace('}', '').split(','),
                   Ips=playerDict['Ips'].replace('{', '').replace('}', '').split(','),
                   Team=registration, Nomination=nomination)


class LineUp:
    """ Class that represents a line-up of league livePlayers.

        :param lineUp:  A dictionary containing Keyhashes as keys and league livePlayers as values.

            note::  Author(s): Mitch """

    def __init__(self, lineUp: dict = None):
        if lineUp:
            self.lineUp = lineUp
        else:
            self.lineUp = {}

    def __getitem__(self, item):
        if item in self.lineUp:
            return self.lineUp[item]
        else:
            raise ValueError("item " + str(item) + " not in lineUp")

    def __setitem__(self, key, value):
        self.lineUp[key] = value

    def __contains__(self, item):
        if item in self.lineUp:
            return True
        else:
            return False

    def __str__(self):
        return "\n".join([str(player) for player in self.lineUp.values()])


LeaguePlayers = LeaguePlayer.storageDict
