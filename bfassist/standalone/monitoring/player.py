#############################################################################
#
#
# Module of BFA introducing and managing Player Class
#
#
#############################################################################
""" This module implements logging of the base player object.

    Dependencies:

        bfassist <- (standalone.monitoring.)player
            |
            |-> bfa_logging
            \-> sql
             -> usersystem

        note::  Author(s): Mitch last-check: 08.07.2021 """

from functools import wraps

from bfassist.bfa_logging import log
from bfassist.sql import *
from bfassist.usersystem import BFAUsers


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Player(DBStorable, table='players', live=False):
    """ A Player is supposed to correspond to a player participating in a BfRound on a bf server hooked with BF-A and
    contains all relevant included intermediary information.
    A player is typically first instantiated from the bfxml module when parsing the event log or by the servers module
    when booting the list of active livePlayers.

    All params are 'private' since they are supposed to be mirrored by the database. Direct manipulation of
    the param would not directly translate to the database. That is why we use setters/getters in this particular case.
    The keyhash has no setter because we don't want it to change. The set of ips and aliases can't be set either
    because we don't want to remove information, we just want to be able to add new ips and aliases.

        :param Keyhash:         The keyhash of a player. (Bots have their name as keyhash)
        :param Alias:           Name the player was first seen with or an otherwise specified nick.
        :param Aliases:         List of other names this player has used on Servers hooked with BF-A.
        :param Clan:            Displays potential association to a bf clan.
        :param Ips:             Set of ips the player has been using on Servers hooked with BF-A.

            note::  Author(s): Mitch """

    def __init__(self, Keyhash: str, Alias: str, Aliases: set = None, Ips: set = None):

        self.SKeyhash = Keyhash, VARCHAR(32), PRIMARY_KEY
        self.SAlias = Alias, VARCHAR(32)
        if Aliases is not None:
            self.SAliases = Aliases, MEDIUMTEXT
        else:
            self.SAliases = {Alias}, MEDIUMTEXT
        if Ips is not None:
            self.SIps = Ips, TEXT
        else:
            self.SIps = set(), TEXT

        self.insertToDB()

    @staticmethod
    def typeHint():
        return {
            'Keyhash': str,
            'Alias': str,
            'Aliases': str,
            'Ips': str
        }

    def toGlobalDict(self):
        """ Function to turn a player into a dictionary of it's attributes and attribute values.

            :return:    Dictionary containing player information.

                note::  Author(s): Mitch """

        return {
            'Keyhash':          self.getKeyhash(),
            'Alias':            self.getAlias(),
            'Aliases':          str(self.getAliases()),
            'Ips':              str(self.getIps() if self.getIps() else '')
        }

    def addAlias(self, inAlias: str):
        """ Function to add an alias to the set of aliases(including database update).

            :param inAlias: The alias to add to the set of aliases of the player.

                note::  Author(s) : Mitch """

        if inAlias in self.getAliases():
            return
        self.getAliases().add(inAlias)
        try:
            self.__class__.storageDict.dbLock.acquire(True)
            self.__class__.storageDict.db.execute("UPDATE livePlayers SET aliases=? WHERE keyhash=?",
                                                  (";".join([x.replace(';', '\\&r01') for x in self.getAliases()]),
                                                   self.getKeyhash(),))
            self.__class__.storageDict.bfaSQLdatabase.commit()
        finally:
            self.__class__.storageDict.dbLock.release()

    def addIp(self, inIp: str):
        """ Function to add an ip to the set of ips(including database update).

            :param inIp: The ip to add to the set of ips of the player.

                note::  Author(s) : Mitch """

        if inIp in self.getIps():
            return
        self.getIps().add(inIp)
        try:
            self.__class__.storageDict.dbLock.acquire(True)
            self.__class__.storageDict.db.execute("UPDATE livePlayers SET ips=? WHERE keyhash=?",
                                                  (";".join(self.getIps()), self.getKeyhash(), ))
            self.__class__.storageDict.bfaSQLdatabase.commit()
        finally:
            self.__class__.storageDict.dbLock.release()


Players = Player.storageDict


def bfaUsersContainsWrapper(func: callable):
    """ A wrapper for the database dictionary contains method to also enable direct checking of player objects rather
    than only their keyhashes.

        :param func:    The contains method that should be wrapped.

            note::  Author(s): Mitch """

    wraps(func)

    def containsWrapper(self, item: Player):
        if isinstance(item, Player):
            return func(self, item.getKeyhash())
        else:
            return func(self, item)
    return containsWrapper


BFAUsers.__contains__ = bfaUsersContainsWrapper(BFAUsers.__contains__)


def bfaUsersSetItemWrapper(func: callable):
    """ A wrapper for the database dictionary set item method to also enable setting for player objects rather than only
     for their keyhashes.

        :param func:    The contains method that should be wrapped.

            note::  Author(s): Mitch """

    wraps(func)

    def setItemWrapper(self, key: Player, value: DBStorable):
        if isinstance(key, Player):
            return func(self, key.getKeyhash(), value)
        else:
            return func(self, key, value)
    return setItemWrapper


BFAUsers.__setitem__ = bfaUsersSetItemWrapper(BFAUsers.__setitem__)


def bfaUsersGetItemWrapper(func: callable):
    """ A wrapper for the database dictionary get item method to also enable getting from player objects rather than
    only from their keyhashes.

        :param func:    The contains method that should be wrapped.

            note::  Author(s): Mitch """

    wraps(func)

    def getItemWrapper(self, item: Player):
        if isinstance(item, Player):
            return func(self, item.getKeyhash(), value)
        else:
            return func(self, key, value)

    return getItemWrapper


BFAUsers.__getitem__ = bfaUsersGetItemWrapper(BFAUsers.__getitem__)
