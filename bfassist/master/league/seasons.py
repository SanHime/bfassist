#############################################################################
#
#
# Module of BFA that manages league activity concerning players
#
#
#############################################################################
""" This module should introduce functionality related to league activity. Especially such that is closely related to
seasons.

    Dependencies:

        bfassist <- (master.league.)seasons
            |
            |-> bfa_logging
            \-> sql
             -> master -> league


        note::  Author(s): Mitch last-check: 07.07.2021 """

from datetime import datetime, timedelta

from bfassist.bfa_logging import log
from bfassist.sql import *
from bfassist.master.league import LeaguePlayers, LeaguePlayer, LeagueTeams, LeagueTeam, LineUp


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


CURRENT_SEASON_NAME = "21a"
CURRENT_SEASON = None


class LeagueSeason(DBStorable, table='seasons', live=False):
    """ Class that represents a bf league season.

        :param SeasonName:          Name of this season also primary key.
        :param ExpectedPlayerCount:      Expected number of participants.

        :param Start:               The scheduled start of the season.
        :param NominationsEnd:      The scheduled end of the nomination phase.
        :param RegistrationsEnd:    The scheduled end of the registration phase.

        :param Nominations:         A set of teams that were nominated for this season.
        :param End:                 The scheduled end of the season.

            note::  Author(s): Mitch """

    def __init__(self, SeasonName: str, ExpectedPlayerCount: int, Start: datetime = None,
                 NominationsEnd: datetime = None, RegistrationsEnd: datetime = None, Nominations: set = None,
                 End: datetime = None):

        self.SSeasonName = SeasonName, VARCHAR(32), PRIMARY_KEY
        self.SExpectedPlayerCount = ExpectedPlayerCount, INTEGER

        if Start:
            self.SStart = Start, DATETIME
        else:
            self.SStart = datetime.now(), DATETIME

        if NominationsEnd:
            self.SNominationsEnd = NominationsEnd, DATETIME
        else:
            self.SNominationsEnd = datetime.now() + timedelta(days=7), DATETIME

        if RegistrationsEnd:
            self.SRegistrationsEnd = RegistrationsEnd, DATETIME
        else:
            self.SRegistrationsEnd = self.getNominationsEnd() + timedelta(days=7), DATETIME

        if Nominations:
            self.SNominations = Nominations, TEXT
        else:
            self.SNominations = set(), TEXT
        self.SEnd = End, DATETIME

        self.insertToDB()

    def nominationsAreOpen(self):
        """ Simple function to find if the nomination phase is ongoing.

            :return:    True if ongoing else false.

                note::  Author(s): Mitch """

        if self.getNominationsEnd() > datetime.now() > self.getStart():
            return True
        else:
            return False

    def registrationsAreOpen(self):
        """ Simple function to find if the registration phase is ongoing.

            :return:    True if ongoing else false.

                note::  Author(s): Mitch """

        if self.getRegistrationsEnd() > datetime.now() > self.getNominationsEnd():
            return True
        else:
            return False

    def attemptNomination(self, nominationAttempt: dict):
        """ Function to be used for attempting a nomination.

            :param nominationAttempt:   The nomination attempt.

            :return:                    True if the nomination attempt is successful otherwise false.

                note::  Author(s): Mitch """

        if self.nominationsAreOpen():
            if nominationAttempt['keyhash'] in LeaguePlayers:
                LeaguePlayers[nominationAttempt['keyhash']].setNomination(nominationAttempt['nomination'])
                return True
            else:
                LeaguePlayer.fromDict(nominationAttempt)
                return True
        else:
            return False

    def attemptRegistration(self, registrationAttempt: dict):
        """ Function to be used for attempting a registration.

            :param registrationAttempt: The registration attempt.

            :return:                    True if the registration attempt is successful otherwise false.

                note::  Author(s): Mitch """

        if self.registrationsAreOpen():
            if not self.getNominations():
                self.finalizeNominations()
            if registrationAttempt['keyhash'] in LeaguePlayers:
                if LeaguePlayers[registrationAttempt['keyhash']].setRegistration(registrationAttempt['registration']):
                    return True
            else:
                player = LeaguePlayer.fromDict(registrationAttempt)
                if player.getTeam():
                    return True

        return False

    def finalizeNominations(self):
        """ Function that finalizes the nomination phase of a season according to the rules of the bf-league specified
        in: https://www.bf-league.eu/index.php?option=com_content&task=view&id=741&Itemid=386&limit=1&limitstart=1#1.0a

                note::  Author(s): Mitch """

        X = self.getExpectedPlayerCount() // 10

        nominations = {}

        for player in LeaguePlayers:
            if player.getNomination().lower() in nominations:
                nominations[player.getNomination().lower()] += 1
            elif player.getNomination().lower() not in nominations:
                nominations[player.getNomination().lower()] = 1

        inv_nominations = {}

        for nomination in sorted(nominations.items(), reverse=True):
            if nomination[1] in inv_nominations:
                inv_nominations[nomination[1]].append(nomination[0])
            else:
                inv_nominations[nomination[1]] = [nomination[0]]

        results = set()

        for x in range(X):
            if inv_nominations:
                results.update(inv_nominations.popitem()[1])

        self.setNominations(results)

    def finalizeTeams(self):
        """ Function that finalizes the registration phase of a season according to the rules of the bf-league specified
        in: https://www.bf-league.eu/index.php?option=com_content&task=view&id=741&Itemid=386&limit=1&limitstart=1#1.0a

                note::  Author(s): Mitch """

        for teamName in self.getNominations():
            if teamName in LeagueTeams:
                team = LeagueTeams[teamName]
                team.setActiveSeasons(team.getActiveSeasons().add(CURRENT_SEASON_NAME))
            else:
                team = LeagueTeam(teamName, {CURRENT_SEASON_NAME})

            players = LineUp()
            for player in LeaguePlayers:
                if player.getTeam() == teamName:
                    players[player.getKeyhash()] = player
                elif player.getNomination() == teamName:
                    players[player.getKeyhash()] = player

            team.setTeamPlayers(players)

    def printTeams(self):
        """ Function to print the teams and livePlayers participating.

                note::  Author(s): Mitch """

        for team in LeagueTeams:
            if self.getSeasonName() in team.getActiveSeasons():
                print(team)

    def setTeamLeaders(self):
        """ Function to manually set the leader of each team.

                note::  Author(s): Mitch """

        for team in LeagueTeams:
            if self.getSeasonName() in team.getActiveSeasons():
                print(team)
                team.setTeamLeader(LeaguePlayers[input("Please enter the keyhash of the team leader>>>")])


LeagueSeasons = LeagueSeason.storageDict

if not CURRENT_SEASON and CURRENT_SEASON_NAME != "" and CURRENT_SEASON_NAME in LeagueSeasons:
    CURRENT_SEASON = LeagueSeasons[CURRENT_SEASON_NAME]
elif CURRENT_SEASON and CURRENT_SEASON_NAME != "" and CURRENT_SEASON_NAME in LeagueSeasons:
    CURRENT_SEASON = LeagueSeasons[CURRENT_SEASON_NAME]
else:
    log("No season running currently.")
