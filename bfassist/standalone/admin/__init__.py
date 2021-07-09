#############################################################################
#
#
#   BFA Standalone Admin Module to BFA c7
#
#
#############################################################################
""" This module handles the traditional in-game bf administration. The api package would make the in-game commands too
long and to clunky to use. A slightly different approach is therefore used. There are a lot of similarities with the
api package though.

Since this involves again the modularisation-problem of the league extensions this module also uses import trickery.

The in-game usage of a command is:

    'currentModulePrefix' + function name as specified in usageOf + arguments

    Each of them need to be separated by a space: ' '.

Bfa will use the usersystem to determine if a player can issue a command and execute it accordingly. Unlike the api
package this in-game interface doesn't use a dedicated object-class to specify/register functions/commands. Rather they
are getting mixed-in via the "usageOf" list and the updateUsageOf function of the administrationcore.

To add a command it's enough to define the command within one of the module classes in the bfa context and adding the
so-created function to the usageOf list. After the class definition the updateUsages method of the core is called and
thereby makes the function/command available from the chat.

    Dependencies:

        admin ----> administrationcore
                |-> administrationbasic
                \-> administrationhenk      (as of now this will be included in the base version)
                 -> administrationleague    (if available)

        note::  Author(s): Mitch last-check: 08.07.2021 """

from os import listdir
from importlib import import_module

from bfassist.standalone.admin.administrationcore import ServerAdministrationCore


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


ServerAdministration = ServerAdministrationCore

try:
    for file in listdir('bfassist/standalone/admin/'):
        if file.endswith('.py') and not (file.startswith('__init__') or file.startswith('administrationcore')):
            import_module('bfassist.standalone.admin.' + file[:-3])
except FileNotFoundError:
    print("Using module outside of valid bfa environment. Commencing without setting up admin for bfa standalone.")
