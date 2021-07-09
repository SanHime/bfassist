#############################################################################
#
#
# Module of BFA that manages league activity concerning players
#
#
#############################################################################
""" This module should introduce functionality related to league activity. Especially such that is closely related to
teams.

    Dependencies:

        bfassist <- (master.league.)teams
            |
            \-> sql
             -> master -> league


        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from bfassist.sql import *
from bfassist.master.league import LeaguePlayers, LeaguePlayer, LineUp


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def pyPlayerToSQL(inPlayer: LeaguePlayer):
    if inPlayer is not None:
        return inPlayer.getKeyhash()
    else:
        return ""


def pyLineUpToSQL(inLineUp: LineUp):
    return ";".join([keyhash.replace(';', '\\&r01') if keyhash else '' for keyhash in inLineUp.lineUp])


def sqlPlayerToPy(sql: str):
    if sql in LeaguePlayers:
        return LeaguePlayers[sql]
    else:
        return str(sql)


def sqlLineUpToPy(sql: str):
    lineUp = LineUp()
    for keyhash in set([x.replace('\\&r01', ';') for x in sql.split(';')]):
        if keyhash in LeaguePlayers:
            lineUp[keyhash] = LeaguePlayers[keyhash]
    return lineUp


class LeagueTeam(DBStorable, table="teams", live=False):
    """ Class that represents a team participating in a league season.

        :param TeamName:        The name of this team.
        :param TeamLeader:      The team leader of this team.
        :param TeamPlayers:     The league livePlayers of this team as line-up.
        :param ActiveSeasons:   Names of the seasons this team was active.

            note::  Author(s): Mitch """

    def __init__(self, TeamName: str, ActiveSeasons: set, TeamLeader: LeaguePlayer = None, TeamPlayers: LineUp = None):
        if not self.initialised:
            self.addConversions(
                (pyPlayerToSQL, sqlPlayerToPy),
                (pyLineUpToSQL, sqlLineUpToPy)
            )

        self.STeamName = TeamName, VARCHAR(32), PRIMARY_KEY
        self.SActiveSeasons = ActiveSeasons, TINYTEXT
        self.STeamLeader = TeamLeader, VARCHAR(32)
        if TeamPlayers:
            self.STeamPlayers = TeamPlayers, TEXT
        else:
            self.STeamPlayers = LineUp(), TEXT

        self.insertToDB()

    def __str__(self):
        return self.getTeamName() + "\n\nTeam Leader:\t" + str(self.getTeamLeader()) + "\n\nLine Up:\n\n" +\
               str(self.getTeamPlayers())


LeagueTeams = LeagueTeam.storageDict
