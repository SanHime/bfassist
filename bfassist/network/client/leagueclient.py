#############################################################################
#
#
#   League Client network Client Module to BFA c7
#
#
#############################################################################
""" This module defines the league client as an extension to the base client for making requests to the bfa master that
concern functionality of the bf league. Comments in this file and the corresponding server file are used to keep
associated client and server functions aligned on the same line of code.

    Dependencies:

        bfassist <- (network.client.)leagueclient
            |
            |-> standalone
            |-> standalone -> monitoring
            \-> bfa_logging
             -> network -> client

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

import json

from bfassist.standalone import Player
from bfassist.standalone.monitoring import BfRound
from bfassist.bfa_logging import log

from bfassist.network.client import BFA_CLIENT, BFABaseClient


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class LeagueClientExtension(BFABaseClient):
    """ An extension of the bfa base client that incorporates requests required by the bf league.

            note::  Author(s): Mitch """

    def sendLeagueRound(self, inRound: BfRound):
        """ This function sends a league round to the master.

            :param inRound: The round to set.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall('LeagueRound'):
            return False
        self.sendAsJSON(inRound.toGlobalDict())
        self.disconnect()

    def sendPlayer(self, inPlayer: Player, add: dict = None):
        """ Simple function to transmit a player in a serialised way plus some optional extra data.

            :param inPlayer:    The player to transmit.
            :param add:         The extra data to transmit in a dictionary.

            :return:            True if processed as expected, false otherwise.

                note::  Author(s): Mitch """

        try:
            if isinstance(inPlayer, Player):
                message = inPlayer.toGlobalDict()
                if add:
                    message.update(add)
                self.sendAsJSON(message)
                return True
            else:
                log("Error: " + str(inPlayer) + " was not a player object.", 4)
                self.sendAsJSON({})
                return False
        except TimeoutError:
            log("Error: Timeout while sending a player object.", 3)
            return False

    def sendPlayers(self, inPlayers: list):
        """ Simple function to transmit a list of livePlayers as dictionary in a serialised way.

            :return:    True if processed as expected, false otherwise.

                note::  Author(s): Mitch """
        try:
            self.sendAsJSON(inPlayers)
            return True
        except BrokenPipeError:
            self.disconnect()
            self.connect()
            return self.sendPlayers(inPlayers)

    def checkPlayer(self, inPlayer: Player):
        """ This function transmits player information to bfa master to check if they are a league player.

            :param inPlayer:    The player to check.

            :return:            True if the player is a league player otherwise false.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall("CheckPlayer"):
            return False
        if not self.sendPlayer(inPlayer):
            return False

        return self.handleResponse(
            expected='Success: Player is a league player.',
            success="Player " + inPlayer.getFirstseenornick() + " is a league player.",
            failure="Player " + inPlayer.getFirstseenornick() + " is not a league player."
        )

    def checkPlayerIsLeader(self, inPlayer: Player):
        """ This functions transmits player information to bfa master to check if they are a league team leader.

            :param inPlayer:    The player to check.

            :return             True if the player is a league player otherwise false.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall("CheckPlayerIsLeader"):
            return False
        if not self.sendPlayer(inPlayer):
            return False

        return self.handleResponse(
            expected='Success: Player is a league team leader.',
            success="Player " + inPlayer.getFirstseenornick() + " is a league team leader.",
            failure="Player " + inPlayer.getFirstseenornick() + " is not a league team leader."
        )

    def sendLeagueNomination(self, nominator: Player, nominated: str):
        """ This function transmits a league nomination to the master server.

            :param nominator:   The player nominating a team.
            :param nominated:   The team this player nominates.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall('LeagueNomination', failure="Error: Transmission of league nomination failed!"):
            return False
        if not self.sendPlayer(nominator, add={'nomination': nominated}):
            return False

        return self.handleResponse(
            expected='Success: League nomination was transmitted.',
            success="League nomination by " + nominator.getFirstseenornick() + " for " + nominated +
                    " was successfully transmitted to the master server.",
            failure="Error: Transmission of league nomination failed!"
        )

    def sendLeagueRegistration(self, registrator: Player, registrated: str):
        """ This function transmits a league registration to the master server.

            :param registrator: The player registering for a team.
            :param registrated: The team this player registers for.

            :return:            True if successful otherwise false.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall('LeagueRegistration'):
            return False
        if not self.sendPlayer(registrator, add={'registration': registrated}):
            return False

        return self.handleResponse(
            expected='Success: League registration was transmitted.',
            success="League registration by " + registrator.getFirstseenornick() + " for " + registrated +
                    " was successfully transmitted to the master server.",
            failure="Error: Transmission of league registration failed!"
        )

    def checkBinary(self, inDigest: str):
        """ This function transmits the sha-256 digest of the dynamic binary matches with that of the league binary.

            :param inDigest:    The sha-256 digest.

            :return:            True if the digest matches otherwise false.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall("CheckBinary"):
            return False
        self.sendString(inDigest)

        return self.handleResponse(
            expected='Success: Hashes match.'
        )

    def requestActiveMaps(self):
        """ This functions requests a dictionary of map names and their respective hex-digest.

            :return:    Dictionary containing active map names as keys and their hex-digest as values.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall("ActiveMaps"):
            return False

        j = self.receiveJSON()
        self.disconnect()
        return j

    def getLeagueSettings(self):
        """ This function demands the league standard settings as dictionary from the bfa master.

            :return:    The league standard settings as dictionary.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall('LeagueSettings'):
            self.disconnect()
            return False
        j = self.receiveJSON()
        self.disconnect()
        return j

    def updateLeaguePlayers(self, inPlayers: dict):
        """ This function send an update containing all livePlayers of an onlinePlayers dictionary of a server to the
        bfa master.

            :param inPlayers:   The dictionary containing playerIds and the corresponding Player object.

                note::  Author(s): Mitch """

        if not self.declareRemoteCall('UpdateLeaguePlayers'):
            return False
        to_send = []
        for Id in inPlayers:
            to_send.append(inPlayers[Id].toGlobalDict())
        if not self.sendPlayers(to_send):
            return False
        return True

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


# noinspection PyRedeclaration
BFA_CLIENT = LeagueClientExtension()

#   # Server client_requests.update
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
