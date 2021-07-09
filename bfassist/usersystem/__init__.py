#############################################################################
#
#
#   BFA User System Module to BFA c7
#
#
#############################################################################
""" This module defines a very simplistic user system utilised in bfa. A user is by default primarily defined by its
keyhash. A 'unique' identifier in bf generated from the cd-key in a 'not-anymore-100%-secure' procedure. This keyhash
is enough for the in-game interface to authenticate a player. For the webservice/api a username/password combination are
also required for authentication.

The user-info is stored in the database. Currently un-encrypted, should be a todo:: to add encryption.

    Dependencies:

        usersystem -\-> bfarights
                     -> bfauser

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.usersystem.bfarights import BFARight
from bfassist.usersystem.bfauser import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass
