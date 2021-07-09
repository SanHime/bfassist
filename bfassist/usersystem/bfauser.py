#############################################################################
#
#
#   BFA User System - BFA User Module to BFA c7
#
#
#############################################################################
""" This module defines the users that can use functions and features of bfa. Bfa users are stored in the database table
called 'privileges'.

    Dependencies:

        bfassist <- usersystem <- bfauser
            |
            \-> sql
             -> bfa_logging

        todo::  Add password-encryption.
        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.usersystem import BFARight
from bfassist.sql import *
from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


SuperAdmin = BFARight('SuperAdmin')
Admin = BFARight('Admin')
Default = BFARight('Default')
Rightless = BFARight('Rightless')


def pyRightToSQL(inRight: BFARight):
    """ Simple function for converting a python bfa right to a database insertable string using the name of the right.

        :param inRight: The right to insert to the database.

        :return:        The string for insertion to the database.

            note::  Author(s): Mitch """

    return inRight.Name


def sqlRightToPy(sql: str):
    """ Simple function for casting sql returns to a bfa right.

        :param sql: The sql return.

        :return:    The python bfa right.

            note::  Author(s): Mitch """
    return BFARight(sql)


class BFAUser(DBStorable, table='privileges', live=True):
    """ Class that represents a user of BF-A.

        :param Keyhash:         The keyhash associated with the bfa user.
        :param Rights:          The bfa rights associated with the bfa user.
        :param User:            The web username of the bfa user.
        :param Pass:            The web password of the bfa user.
        :param Online:          The number of times this user is logged-in.
        :param MultiLogin:      Whether multiple web login are permitted.

            note::  Author(s): Mitch """

    def __init__(self, Keyhash: str, Rights: BFARight = Default, User: str = None, Pass: str = None, Online: int = 0,
                 MultiLogin: bool = False):
        if not self.initialised:
            self.addConversion(pyRightToSQL, sqlRightToPy)

        self.SKeyhash = Keyhash, VARCHAR(32), PRIMARY_KEY
        self.SRights = Rights, VARCHAR(255)
        self.SUser = User, VARCHAR(32)
        self.SPass = Pass, VARCHAR(32)
        self.SOnline = Online, TINYINT
        self.SMultiLogin = MultiLogin, BIT

        self.insertToDB()

    def editUser(self, newKeyhash: str, newRights: str, newMultiLogin: str):
        """ Simple function that edits a bfa user.

            :param newKeyhash:      The new keyhash to be set.
            :param newRights:       The new rights to be set.
            :param newMultiLogin:   Whether multiple web logins are now permitted.

            :return True:           At the end of the edit procedure.

                note::  Author(s): Mitch """
        try:
            newRights = BFARight(newRights)
            self.setRights(newRights)
        except ValueError:
            pass
        if newMultiLogin in ['True', 'true', '1']:
            self.setMultiLogin(True)
        elif MultiLogin in ['False', 'false', '0']:
            self.setMultiLogin(False)
        if newKeyhash != '':
            self.setKeyhash(newKeyhash)
        return True

    def isOnline(self):
        """ Gets online status of a user.

            :return:    True if the user is online at least once, otherwise False.

                note::  Author(s): Mitch """

        return bool(self.getOnline())

    def allowsMultipleLogins(self):
        """ Gets if this user permits multiple log-ins

            :return:    True if the user is allowed to log-in multiple times, otherwise False.

                note::  Author(s): Mitch """

        return self.getMultiLogin()

    def credentialsMatch(self, inUser: str, inPw: str):
        """ Checks if credentials meet.

            :param inUser:  Username.
            :param inPw:    Password.

            :return:    True if correct, False otherwise.

                note::  Author(s): Mitch """

        if self.getUser() == inUser and self.getPass() == inPw:
            return True
        else:
            return False

    def isRegistered(self):
        """ Function to find if a user is already registered for the webservice.

            :return:    True if already registered False otherwise.

                note::  Author(s): Mitch """

        if self.getUser() is None:
            return False
        else:
            return True

    def login(self):
        """ Logs a user in and therefore increments the online counter by one.

                note::  Author(s): Mitch """

        self.setOnline(self.getOnline() + 1)

    def logout(self):
        """ Logs a user out and therefore decrements the online counter by one.

                note::  Author(s): Mitch """

        self.setOnline(self.getOnline() - 1)

    @staticmethod
    def typeHint():
        return {
            'Keyhash': str,
            'Rights': BFARight.typeHint(),
            'User': str,
            'Pass': str,
            'Online': int,
            'MultiLogin': bool
        }

    def toLocalDict(self):
        """ Function to retrieve this bfa user as a dictionary with attributes as anchors and their values.

            :return:    Dictionary representation of this user.

                note::  Author(s): Mitch """

        return {
            'Keyhash':      self.getKeyhash(),
            'Rights':       self.getRights().toLocalDict(),
            'User':         self.getUser(),
            'Pass':         self.getPass(),
            'Online':       self.getOnline(),
            'MultiLogin':   self.getMultiLogin()
        }


BFAUsers = BFAUser.storageDict


if not BFAUsers.liveSet:
    log("No bfa user found. Adding setup user.")
    BFAUser('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', SuperAdmin, 'admin', 'password', 0, False)

for bfaUser in BFAUsers.liveSet:
    if bfaUser.getOnline() > 0:
        bfaUser.setOnline(0)
