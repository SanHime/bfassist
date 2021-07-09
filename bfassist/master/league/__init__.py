#############################################################################
#
#
# Module of BFA that manages league activity
#
#
#############################################################################
""" This module introduces functionality related to activity of the bf-league at bf-league.eu .
Everything here is therefore quite BF focused.

    Dependencies:

        league ---> players
                |-> teams
                |-> seasons
                \-> servers
                 -> bflstatistics

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.master.league.players import LeaguePlayers, LeaguePlayer, LineUp
from bfassist.master.league.teams import LeagueTeams, LeagueTeam
from bfassist.master.league.seasons import *
from bfassist.master.league.servers import *
from bfassist.master.league.bflstatistics import LeagueRound, LeagueRounds, BfPlayerRound, BfPlayerRounds


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass
