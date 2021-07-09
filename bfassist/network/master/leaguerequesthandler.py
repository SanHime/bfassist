#############################################################################
#
#
#   League Request Handler network Module to BFA Master
#
#
#############################################################################
""" This module defines the league request handler as an extension to the base request handler for handling requests
to the bfa master that were made by the clients. Comments in this file and the corresponding client file are used to
keep associated client and server functions aligned on the same line of code.

    Dependencies:

        bfassist <- (network.)master <- leaguerequesthandler
            \
             -> master -> league

        note::  Author(s): Mitch last-check: 07.07.2021 """

from pathlib import Path

from bfassist.network.master import ThreadedTCPRequestHandler
import bfassist.master.league as bfl


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


#
#
#
#
#
#


class LeagueMasterExtension(ThreadedTCPRequestHandler):
    """ An extension of the bfa base request handler that incorporates handling of requests required by the bf league.

        note::  Author(s): Mitch """

    def receiveLeagueRound(self):
        """ This function receives a bf round that should have been part or a league match and saves it to the database.

                note::  Author(s): Mitch """

        league_round = self.receiveJSON()
        if not league_round:
            return
        bfl.LeagueRound.fromDict(league_round)

    #
    #
    #   # Client sendPlayer
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #   # Client sendPlayers
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    def checkPlayer(self):
        """ Check if a player is part of the league livePlayers.

                note::  Author(s): Mitch """

        player = self.receiveJSON()
        if player is None:
            return
        if player['keyhash'] in bfl.LeaguePlayers:
            self.sendString('Success: Player is a league player.')
        else:
            self.sendString('Failure: Player is not a league player.')

    #
    #
    #
    #
    #
    #

    def checkPlayerIsLeader(self):
        """ Check if a player is part of the league livePlayers.

                        note::  Author(s): Mitch """

        player = self.receiveJSON()
        if player is None:
            return
        if player['keyhash'] in bfl.LeaguePlayers:
            if bfl.LeaguePlayers[player['keyhash']].isLeader():
                self.sendString('Success: Player is a league team leader.')
            else:
                self.sendString('Failure: Player is not a league team leader.')
        else:
            self.sendString('Failure: Player is not a league team leader.')

    #
    #
    #

    def receiveLeagueNomination(self):
        """ Receive a league nomination from a client.

                note::  Author(s): Mitch """

        league_nomination = self.receiveJSON()
        if league_nomination is None:
            return
        else:
            if bfl.CURRENT_SEASON.attemptNomination(league_nomination):
                self.sendString('Success: League nomination was transmitted.')
            else:
                self.sendString('Failure: League nomination was unsuccessful.')

    #
    #
    #
    #
    #

    def receiveLeagueRegistration(self):
        """ Receive a league registration from a client.

                note::  Author(s): Mitch """

        league_registration = self.receiveJSON()

        if league_registration is None:
            return

        else:
            if bfl.CURRENT_SEASON.attemptRegistration(league_registration):
                self.sendString('Success: League registration was transmitted.')
            else:
                self.sendString('Failure: League registration was unsuccessful.')

    #
    #
    #
    #
    #

    def checkBinary(self):
        """ Check if the digest of a dynamic binary matches with the one of the league binary.

                note::  Author(s): Mitch """

        clientBinaryHash = self.getRequest()
        if exists('bfassist/references/league/binaries/league.dynamic'):
            if clientBinaryHash == self.shaForFile('bfassist/references/league/binaries/league.dynamic'):
                self.sendString('Success: Hashes match.')
            else:
                self.sendString('Failure: Hashes do not match.')
        else:
            self.sendString('Failure: Could not find the corresponding dynamic binaries.')

    #
    #

    def sendActiveMaps(self):
        """ Sends JSON containing a dictionary of the names of the active map files and their hex-digest.

                note::  Author(s): Mitch """

        # todo:: Check if this is still required
        map_path = Path('bfassist/references/league/maps/' + bfl.CURRENT_SEASON_NAME + '/')
        signature = self.createFolderSignature(map_path)

        for mapName in set(signature.keys()):
            signature[mapName[1:]] = signature[mapName]
            signature.pop(mapName)
        self.sendAsJSON(signature)

    def sendLeagueSettings(self):
        """ This function sends the standard league settings as dictionary.

                note::  Author(s): Mitch """

        self.sendAsJSON(bfl.LEAGUE_SETTINGS)

    #
    #
    #
    #
    #
    #

    def updateLeaguePlayers(self):
        """ This function receives an update containing player objects as dictionaries that participated in league
        activity.

                note::  Author(s): Mitch """

        player_list = self.receiveJSON()
        if not player_list or len(player_list) == 0:
            return
        for player_dict in player_list:
            if player_dict['keyhash'] in bfl.LeaguePlayers:
                self.updateLeaguePlayer(bfl.LeaguePlayers[player_dict['keyhash']], player_dict)
            else:
                bfl.LeaguePlayer.fromDict(player_dict)

    #

    @staticmethod
    def updateLeaguePlayer(inPlayer: bfl.LeaguePlayer, playerDict: dict):
        """ Simple function that updates the information of a known league player with new information from a dict.

                note::  Author(s): Mitch """

        for alias in playerDict['aliases']:
            if alias not in inPlayer.getAliases():
                inPlayer.addAlias(alias)
        for ip in playerDict['ips']:
            if ip not in inPlayer.getIps():
                inPlayer.addIp(ip)


ThreadedTCPRequestHandler = LeagueMasterExtension

ThreadedTCPRequestHandler.client_requests.update({
        "LeagueNomination":     ThreadedTCPRequestHandler.receiveLeagueNomination,
        "LeagueRegistration":   ThreadedTCPRequestHandler.receiveLeagueRegistration,
        "CheckPlayer":          ThreadedTCPRequestHandler.checkPlayer,
        "CheckBinary":          ThreadedTCPRequestHandler.checkBinary,
        "CheckPlayerIsLeader":  ThreadedTCPRequestHandler.checkPlayerIsLeader,
        "ActiveMaps":           ThreadedTCPRequestHandler.sendActiveMaps,
        "LeagueSettings":       ThreadedTCPRequestHandler.sendLeagueSettings,
        "UpdateLeaguePlayers":  ThreadedTCPRequestHandler.updateLeaguePlayers,
        'LeagueRound':          ThreadedTCPRequestHandler.receiveLeagueRound
})
