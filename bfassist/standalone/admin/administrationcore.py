#############################################################################
#
#
#   BFA Standalone Administration Module to BFA c7
#
#
#############################################################################
""" This module provides the core administrative infrastructure for the administration of a bf server.

    Dependencies:

        2nd-party dependency numpy

        bfassist <- (standalone.admin.)administrationcore
            |
            |-> bfa_logging
            |-> standalone
            \-> usersystem
             -> standalone  @ServerAdministrationCore.bfaStop

        note::  Author(s): Mitch last-check: 08.07.2021 """

from datetime import datetime
from inspect import signature

from numpy import array

from bfassist.bfa_logging import log
from bfassist.standalone import Server
from bfassist.usersystem import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ServerAdministrationCore:
    """ Central unit for the administration of a server.

        :param server:          The server to administer.
        :param triggerPrefixes: A set of prefixes that when read in chat will trigger further progression.

        :param inGameCommands:  A dictionary containing in-game commands as keys and a rights threshold plus function to
                                execute

            note::  Author(s): Mitch """

    currentModulePrefix = 'bfa'
    triggers = {currentModulePrefix}
    inGameCommands = {currentModulePrefix: {}}
    usageOf = []

    def __init__(self, server: Server, triggerPrefixes: set = None):
        self.server = server
        if triggerPrefixes:
            self.triggerPrefixes = triggerPrefixes
        else:
            self.triggerPrefixes = self.triggers

    @classmethod
    def updateUsageOf(cls, func: callable, inGameCommand: str, rightsThreshold: BFARight):
        """ An init that actually makes a function available to be called from the in-game chat.

            :param func:            The function that's getting wrapped and should be available from in-game.
            :param inGameCommand:   The in-game command by which the function should be callable.
            :param rightsThreshold: The minimum bfa rights someone has to hold in order to call the function.

                note::  Author(s): Mitch """

        cls.inGameCommands[cls.currentModulePrefix][inGameCommand] = {'rightsThreshold': rightsThreshold, 'func': func}

    @classmethod
    def updateUsages(cls):
        """ An init that calls the updateUsageOf for all updates specified in usageOf.

                note::  Author(s): Mitch """

        for usage in cls.usageOf:
            cls.updateUsageOf(*usage)

    def bfaStop(self):
        """ This function stops the BFA monitoring entirely.

                note::  Author(s) Mitch """

        from bfassist.standalone import KERN

        log("Received stop from the highest level.")
        KERN.writeToAllServers("BFA received stop signal and is going offline.")
        KERN.stop()
    usageOf += [(bfaStop, 'stop', SuperAdmin)]

    def grantSuper(self, player_id: int):
        """ This function grants bfa0 rights to a player specified by player id on the respective server.

            :param player_id:   Player id of the player to be bfa-master.

                note::  Author(s) Mitch """

        log("Received grantSuper.")
        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            player_keyhash = self.server.PlayerInterface.onlinePlayerWithId[player_id].getKeyhash()
            if player_keyhash not in BFAUsers:
                BFAUser(player_keyhash, SuperAdmin)
                self.server.ConsoleInterface.writeToServer("Super-Admin rights granted!")
                log("Granted Super-Admin to a new player.")
            else:
                inserver.writeToServer("This player is already a bfa user.")
    usageOf += [(grantSuper, 'grantSuper', SuperAdmin)]

    def grantAdmin(self, player_id: int):
        """ This function grants bfa1 rights to a player specified by player id on the respective server.

            :param player_id:   Player id of the player to be bfa-admin.

                note:: Author(s) Mitch """

        log("Received grantAdmin.")
        if player_id in self.server.PlayerInterface.onlinePlayerWithId:
            player_keyhash = self.server.PlayerInterface.onlinePlayerWithId[player_id].getKeyhash()
            if player_keyhash not in BFAUsers:
                BFAUser(player_keyhash, Admin)
                self.server.ConsoleInterface.writeToServer("Admin rights granted!")
                log("Granted Admin to a new player.")
            else:
                inserver.writeToServer("This player is already a bfa user.")
    usageOf += [(grantAdmin, 'grantAdmin', Admin)]

    def listenToChat(self, chatMessage: str, player_id: int, player_position: array):
        """ This function listens to the chat messages on the server and takes action if so requested in the chat.

            :param chatMessage:     Potential bfa-command string.
            :param player_id:       Player issuing the command.
            :param player_position: Position the command was issued from.

                note::  Author(s): Mitch """

        triggered = None
        for prefix in self.triggerPrefixes:
            if chatMessage.startswith(prefix):
                triggered = prefix

        if triggered is None:
            pass
        else:
            instruction = chatMessage[len(triggered):].split(' ')
            if not instruction:
                pass
            else:
                command = instruction[0]
                if command not in self.inGameCommands:
                    pass
                else:
                    issuingPlayer = self.server.PlayerInterface.onlinePlayerWithId[player_id]
                    inGameCommand = self.inGameCommands[command]
                    if inGameCommand['rightsThreshold'] > Default:
                        if issuingPlayer not in BFAUsers:
                            pass
                        else:
                            if BFAUsers[issuingPlayer].getRights() < inGameCommand['rightsThreshold']:
                                pass
                            else:
                                funcSignature = signature(inGameCommand['func'])
                                if len(instruction) > 1:
                                    arguments = instruction[1:]
                                else:
                                    arguments = []
                                keywordArguments = {}
                                if 'player_id' in funcSignature:
                                    keywordArguments['player_id'] = player_id
                                if 'player_position' in funcSignature:
                                    keywordArguments['player_position'] = player_position
                                inGameCommand['func'](*arguments, **keywordArguments)

                    else:
                        if issuingPlayer in BFAUsers and BFAUsers[issuingPlayer].getRights() == Rightless:
                            pass
                        else:
                            funcSignature = signature(inGameCommand['func'])
                            if len(instruction) > 1:
                                arguments = instruction[1:]
                            else:
                                arguments = []
                            keywordArguments = {}
                            if 'player_id' in funcSignature:
                                keywordArguments['player_id'] = player_id
                            if 'player_position' in funcSignature:
                                keywordArguments['player_position'] = player_position
                            inGameCommand['func'](*arguments, **keywordArguments)

    @staticmethod
    def typeHintInGameCommands():
        return {
            '__type__': dict,
            '__keys__': str,
            '__values__': {
                '__type__': dict,
                '__keys__': str,
                '__values__': {
                    'rightsThreshold': BFARight.typeHint(),
                    'func': str
                }
            }
        }

    @classmethod
    def listInGameCommands(cls):
        return {
            modulePrefix: {
                inGameCommand: {
                    "rightsThreshold":
                        cls.inGameCommands[modulePrefix][inGameCommand]['rightsThreshold'].toLocalDict(),
                    "func":
                        cls.inGameCommands[modulePrefix][inGameCommand]['func'].__name__
                }
                for inGameCommand in cls.inGameCommands[modulePrefix]
            } for modulePrefix in cls.inGameCommands
        }


ServerAdministrationCore.updateUsages()
