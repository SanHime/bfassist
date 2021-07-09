#############################################################################
#
#
#   Webservice Session Management for BFA
#
#
#############################################################################
""" This provides the session management for the webservice. In particular it limits the session length for a
particular user.

    Dependencies:

        bfassist <- (webservice.)requesthandler <- sessionmanagement
            \
             -> usersystem

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from threading import Thread
from http.cookies import SimpleCookie
from datetime import datetime, timezone
from time import sleep

from bfassist.usersystem import BFAUser


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class SessionManagement(Thread):
    """ Session manager to make sure people are not logged in indefinitely.

        :param sessionLimit:    Session length in minutes.

            note::  Author(s): Mitch """

    clients = {}

    def __init__(self, sessionLimit: int = 15):
        Thread.__init__(self)
        self.stopper = False
        self.sessionLimit = sessionLimit

    def run(self):
        while not self.stopper:
            for client in self.clients:
                if self.clients[client].cookie != 'expired' and datetime.now(timezone.utc).timestamp() -\
                        self.clients[client].loginTime.timestamp() > 60 * self.sessionLimit:
                    self.clients[client].cookie = 'expired'
            sleep(60)
        for client in self.clients:
            if client.bfa_user.getLogin() > 0:
                client.bfa_user.toggleLogin()

    def addClient(self, client_address: tuple, client: BFAUser, cookie: SimpleCookie, loginTime: datetime):
        """ Simple function to add a client/user to the session management.

            :param client_address:  The client address of this user. A tuple containing ip and port.
            :param client:          The bfa-user to create a client/user session for.
            :param cookie:          The cookie that will be assigned to this client/user.
            :param loginTime:       The UTC timestamp of the login.

                note::  Author(s): Mitch """

        self.clients[client_address[0]] = User(client_address, client, cookie, loginTime)
        client.login()

    def removeClient(self, client: User):
        """ Simple function to remove a client from the session management.

            :param client:  The user/client to remove.

                note::  Author(s): Mitch """

        self.clients.pop(client.client_address[0])
        if client.isOnlyLogin(self):
            client.bfa_user.logout()


class User:
    """ Class to model a web service user.

        :param client_address:  The client address of this user. A tuple containing ip and port.
        :param bfa_user:        The bfa user used by this user.
        :param cookie:          The cookie associated with this user.
        :param loginTime:       The UTC timestamp of the login.

            note::  Author(s): Mitch """

    def __init__(self, client_address: tuple, bfa_user: BFAUser, cookie: SimpleCookie, loginTime: datetime):
        self.client_address = client_address
        self.bfa_user = bfa_user
        self.cookie = cookie
        self.loginTime = loginTime

    def isOnlyLogin(self, sessionManager: SessionManagement):
        """ Checks if this users associated bfa user is not allowed to login multiple times or if so if it's the only
        user currently using this bfa_user.

            :param sessionManager:  The session Management this user is managed by.

            :return:                True if it's the only user logged in for its bfa user. False otherwise.

                note::  Author(s): Mitch """

        if self.bfa_user.getMultiLogin():
            for client in sessionManager.clients:
                if sessionManager.clients[client].bfa_user.getKeyhash() == self.bfa_user.getKeyhash():
                    return False
        return True
