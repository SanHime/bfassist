#############################################################################
#
#
#   BFA Standalone League Administration Module to BFA c7
#
#
#############################################################################
""" This module provides everything required for administration of bf-league activities.

    Dependencies:

        bfassist <- standalone <- admin <- administrationleague
            |
            |-> network -> client
            |-> references
            \-> standalone
             -> usersystem

        note::  Author(s): Mitch last-check: 08.07.2021 """

from os.path import exists
from os import listdir
from functools import wraps

from bfassist.standalone.admin import ServerAdministration
from bfassist.standalone import Player
from bfassist.network.client import BFA_CLIENT
from bfassist.references import Binary, Binaries, Map, Maps, listFMapNames
from bfassist.standalone import Server
from bfassist.usersystem import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def usePlayer(func: callable):
    """ Decorator to convert the player_id to a player before passing on the function.

        :param func:    The function to decorate.

            note::  Author(s): Mitch """

    wraps(func)

    def playerIdToPlayerWrapper(*args, **kwargs):
        if 'player_id' in kwargs:
            player = self.server.PlayerInterface.onlinePlayerWithId[kwargs['player_id']]
            kwargs.pop('player_id')
            kwargs['player'] = player
        value = func(*args, **kwargs)
        return value

    return playerIdToPlayerWrapper


class LeagueAdministration(ServerAdministration):
    """ Extension of the server administration that handles bf-league related administrative tasks.

        :param server:          The server this administration extension belongs to.
        :param modulePrefix:    The prefix that applies to the functions described in this module.

            note::  Author(s): Mitch """

    currentModulePrefix = 'bfl'
    ServerAdministration.triggers.add(currentModulePrefix)
    ServerAdministration.inGameCommands[currentModulePrefix] = {}
    usageOf = []

    def __init__(self, server: Server):
        super().__init__(server)

    @usePlayer
    def nominate(self, player: Player, teamName: str):
        """ This function lets a player nominate a team for a bf-league season.

            :param player:      The player object of the player issuing the nomination.
            :param teamName:    Name of the team this play nominates.

                note::  Author(s): Mitch """

        if BFA_CLIENT.sendLeagueNomination(player, teamName):
            self.server.ConsoleInterface.writeToServer('Nomination was successful!')
        else:
            self.server.ConsoleInterface.writeToServer('Nomination failed!')
    usageOf += [(nominate, 'nominate', Default)]

    @usePlayer
    def register(self, player: Player, teamName: str):
        """ This function lets a player register himself with a team for a bf-league season.

            :param player:      The player object of the player issuing the nomination.
            :param teamName:    Name of the team this play nominates.

                note::  Author(s): Mitch """

        if BFA_CLIENT.sendLeagueRegistration(player, teamName):
            self.server.ConsoleInterface.writeToServer('Registration was successful!')
        else:
            self.server.ConsoleInterface.writeToServer('Registration failed!')
    usageOf += [(register, 'register', Default)]

    @usePlayer
    def checkBinaries(self, player: Player):
        """ This function lets a league player check if the correct binaries are in place.
        ::important::   This actually only checks the dynamic binary and assumes binaries are always actually switched
        in pairs!

            :param player:  The player object of the player issuing the nomination.

                note::  Author(s): Mitch """

        if BFA_CLIENT.checkPlayer(player):
            self.server.ExecutableInterface.refreshBinaries()
            binary = self.server.ExecutableInterface.dynamicExecutable
            binaryName = binary.getName()
            binaryCS = binary.getDigest()
            if binaryName == 'league.dynamic':
                self.server.ConsoleInterface.writeToServer("league binaries are in place. Comparing checksum...")
            else:
                self.server.ConsoleInterface.writeToServer(binaryName + " binaries are in place. Comparing checksum...")

            if BFA_CLIENT.checkBinary(binaryCS):
                self.server.ConsoleInterface.writeToServer("Checksums match. Binary is correct.")
            else:
                self.server.ConsoleInterface.writeToServer("Checksums did not match! Binary is incorrect!")
        else:
            self.server.ConsoleInterface.writeToServer("Not authorised to check binaries!")
    usageOf += [(checkBinaries, 'checkBinaries', Default)]

    @usePlayer
    def leagueBinaries(self, player: Player):
        """ This function lets any leader of a league team check if the correct binaries are in place and replace them
        if they are not. ::important:: Only the dynamic binaries are considered for the check, assuming that binaries
        are always switched in pairs!

            :param player:  The player object of the player issuing the nomination.

                note::  Author(s): Mitch """

        if BFA_CLIENT.checkPlayerIsLeader(player):
            self.server.ExecutableInterface.refreshBinaries()
            binary = self.server.ExecutableInterface.dynamicExecutable
            binaryName = binary.getName()
            binaryCS = binary.getDigest()
            if binaryName == 'league.dynamic':
                self.server.ConsoleInterface.writeToServer("league binaries are in place.")
                self.server.ConsoleInterface.writeToServer("Comparing checksum...")
            else:
                self.server.ConsoleInterface.writeToServer(binaryName + " binaries are in place.")
                self.server.ConsoleInterface.writeToServer("Comparing checksum...")

            if BFA_CLIENT.checkBinary(binaryCS):
                self.server.ConsoleInterface.writeToServer("Checksums match. Binary is correct.")
            else:
                self.server.ConsoleInterface.writeToServer("Checksums did not match! Binary is incorrect!")
                self.server.ConsoleInterface.writeToServer("Checking if league binaries are available...")
                if 'league.dynamic' in Binaries:
                    self.server.ExecutableInterface.replaceBinaryPair('league')
                else:
                    if exists('bfassist/references/binaries/league/league.static') and \
                            exists('bfassist/references/binaries/league/league.dynamic'):

                        Binary.fromReference('bfassist/references/binaries/league/league.static')
                        Binary.fromReference('bfassist/references/binaries/league/league.dynamic')
                        self.server.ExecutableInterface.replaceBinaryPair('league')
                    else:
                        self.server.ConsoleInterface.writeToServer("League binaries not available. "
                                                                   "Initiating an update...")
                        BFA_CLIENT.getUpdate()
                    if exists('bfassist/references/binaries/league/league.static') and \
                            exists('bfassist/references/binaries/league/league.dynamic'):

                        Binary.fromReference('bfassist/references/binaries/league/league.static')
                        Binary.fromReference('bfassist/references/binaries/league/league.dynamic')
                        self.server.ExecutableInterface.replaceBinaryPair('league')
                    else:
                        self.server.ConsoleInterface.writeToServer("Retrieving binaries via update failed."
                                                                   " Contact an admin please.")

        else:
            self.server.ConsoleInterface.writeToServer("Not authorised to replace binaries!")
    usageOf += [(leagueBinaries, 'leagueBinaries', Default)]

    @usePlayer
    def checkMaps(self, player: Player):
        """ This function lets a league player check if the correct map files are in place on the server.
        ::important::   This does not check if there are other additional patches installed in other files. It does not
        even check if there are any further 'standard' patches with _008.rfa for example.

            :param player:  The player object of the player issuing the nomination.

                note::  Author(s): Mitch """

        if BFA_CLIENT.checkPlayer(player):
            to_check = BFA_CLIENT.requestActiveMaps()
            if to_check:
                for mapName in to_check:
                    if mapName in Maps and Maps[mapName].getDigest() == to_check[mapName] and \
                            self.server.MapInterface.pathToMods + "bf1942/archives/bf1942/levels/" in \
                            Maps[MapName].getPaths():
                        to_check[mapName] = False
                    else:
                        to_check[mapName] = True
                if any(to_check.values()):
                    self.server.ConsoleInterface.writeToServer("At least one map file differs or isn't in place...")
                else:
                    self.server.ConsoleInterface.writeToServer("Check complete. Correct map files are in place.")
            else:
                self.server.ConsoleInterface.writeToServer("Could not find active maps on the master server.")
        else:
            self.server.ConsoleInterface.writeToServer("Not authorised to check maps!")
    usageOf += [(checkMaps, 'checkMaps', Default)]

    @usePlayer
    def leagueMaps(self, player: Player):
        """ This function lets any leader of a league team check if the correct map files are in place and replace them
        if they are not. ::important::   This does not check if there are other additional patches installed in other
        files. It does not even check if there are any further 'standard' patches with _008.rfa for example.

            :param player:  The player object of the player issuing the nomination.

                note::  Author(s): Mitch """

        if BFA_CLIENT.checkPlayerIsLeader(player):
            to_check = BFA_CLIENT.requestActiveMaps()
            for mapName in to_check:
                if mapName in Maps and Maps[mapName].getDigest() == to_check[mapName] and \
                        self.server.MapInterface.pathToMods + \
                        Maps[mapName].getFName()[:Maps[mapName].getFName().rfind('/') + 1] \
                        in Maps[mapName].getPaths():
                    to_check[mapName] = False
            if any(to_check.values()):
                self.server.ConsoleInterface.writeToServer("At least one map file differs or is not in place...")
                self.server.ConsoleInterface.writeToServer("Initiating update...")
                BFA_CLIENT.getUpdate()
                for mapName in to_check:
                    if to_check[mapName]:
                        if mapName not in Maps:
                            for seasonPack in listdir('bfassist/references/maps/league/'):
                                if mapName in listFMapNames('bfassist/references/maps/league/' + seasonPack):
                                    Map.fromReference('bfassist/references/maps/league/' + seasonPack + "/" + mapName)
                                    self.server.MapInterface.addMapFromReference(Maps[mapName])
                        elif Maps.fetchSingleWhere('Digest', to_check[mapName]):
                            currentMap = Maps.fetchSingleWhere('Digest', to_check[mapName])
                            self.server.MapInterface.replaceMapWithVariation(Maps[mapName], currentMap)
                        else:
                            currentMap = Maps[mapName]
                            if self.server.MapInterface.pathToMods + \
                                    currentMap.getFName()[:currentMap.getFName().rfind('/') + 1] \
                                    not in currentMap.getPaths():
                                self.server.MapInterface.addMapFromReference(currentMap)
                            for seasonPack in listdir('bfassist/references/maps/league/'):
                                if mapName in listFMapNames('bfassist/references/maps/league/' + seasonPack):
                                    self.server.MapInterface.replaceMapReferenceWithMapFromReference(
                                        currentMap, 'bfassist/references/maps/league/' + seasonPack + "/" + mapName)

                self.server.ConsoleInterface.writeToServer("Update complete. Correct map files are in place.")
            else:
                self.server.ConsoleInterface.writeToServer("Check complete. Correct map files are in place.")
        else:
            self.server.ConsoleInterface.writeToServer("Not authorised to replace maps!")
    usageOf += [(leagueMaps, 'leagueMaps', Default)]

    @usePlayer
    def live(self, player: Player):
        """ This function will send the stats of the round finished next on this server to the master.

            :param player:  The player object of the player issuing the nomination.

                note::  Author(s): Mitch """

        if BFA_CLIENT.checkPlayer(player):
            settings = BFA_CLIENT.getLeagueSettings()
            if settings:
                if isinstance(self.server.SettingsInterface.settings, dict):
                    inserver.writeToServer("Could not determine server settings please restart the round...")
                else:
                    mismatches = self.server.SettingsInterface.settings.check(settings)
                    if 'GameTime' in mismatches:
                        if mismatches['GameTime'][0] == self.server.ConsoleInterface.getTimeLimit() / 60:
                            self.server.ConsoleInterface.setGameTime(mismatches['GameTime'][0])
                            mismatches.pop('GameTime')
                    if mismatches:
                        self.server.ConsoleInterface.writeToServer("Some settings are not correct. "
                                                                   "Please correct and try again...")

                        for setting in mismatches:
                            self.server.ConsoleInterface.writeToServer(setting + " should be " +
                                                                       str(mismatches[setting][0]) + " but is " +
                                                                       str(mismatches[setting][1]))

                    else:
                        self.server.ConsoleInterface.writeToServer("Server settings are correct. "
                                                                   "The finished round will be sent to the master "
                                                                   "for evaluation.")
                        self.server.MonitoringInterface.bootPlayers()
                        if not BFA_CLIENT.updateLeaguePlayers(self.server.PlayerInterface.onlinePlayerWithId):
                            self.server.ConsoleInterface.writeToServer("There was a problem transmitting the current "
                                                                       "livePlayers to the master.")
                            self.server.ConsoleInterface.writeToServer("Trying to submit the round anyway.")
                        self.server.StatsInterface.realTimeRound.liveRound = True
            else:
                self.server.ConsoleInterface.writeToServer("There was a problem retrieving the league standard settings"
                                                           " from the master server...")
        else:
            self.server.ConsoleInterface.writeToServer("Not authorised to submit a round.")
    usageOf += [(live, 'live', Default)]


ServerAdministration = LeagueAdministration
ServerAdministration.updateUsages()
