#############################################################################
#
#
#   Webservice Request Handling Authentication for BFA
#
#
#############################################################################
""" This provides the authentication request handling functionality for the webservice.

    Dependencies:

        bfassist <- (webservice.)requesthandler <- authentication
            |                       \
            \                        -> sessionmanagement
             -> usersystem

        note::  Author(s): Mitch last-check: 07.07.2021 """

import json
from datetime import datetime, timezone, timedelta
from http.cookies import SimpleCookie
from uuid import uuid4

from bfassist.webservice.requesthandler import CoreRequestHandler
from bfassist.webservice.requesthandler.sessionmanagement import SessionManagement, User
from bfassist.usersystem import BFAUsers


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class AuthenticationRequestHandler(CoreRequestHandler):
    """ The authentication request handler.

            note::  Author(s): Mitch """

    sessionManager = SessionManagement()

    def createSessionCookie(self, creationTime: datetime):
        """ Function to create a session cookie.

            :param creationTime:    The creation time of the cookie, relevant for expiration.

            :return:                The session cookie.

                note::  Author(s): Mitch """

        cookie = SimpleCookie()
        cookie['session_id'] = str(uuid4())
        cookie['session_id']['domain'] = self.headers['Host'][:-4]
        cookie['session_id']['path'] = '/'
        cookie['session_id']['expires'] = (creationTime + timedelta(minutes=self.sessionManager.sessionLimit)).strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        self.send_response(200)
        self.send_header("Set-Cookie", cookie['session_id'].OutputString() + '; SameSite=Strict; Secure')
        return cookie

    def getUser(self):
        """ Simple function to get the current user if he's logged in.

            :return:    The user if logged in, None otherwise.

                note::  Author(s): Mitch """

        user = None

        if self.client_address[0] in self.sessionManager.clients:
            user = self.sessionManager.clients[self.client_address[0]]

        return user

    def isValidSessionOf(self, user: User):
        """ Simple function to check if the session of a user is valid.

            :param user:    The user to check the session for.

                note::  Author(s): Mitch """

        if user is None:
            return False

        userCookie = SimpleCookie(self.headers.get('Cookie'))

        if 'session_id' not in userCookie:
            return False

        if 'session_id' in user.cookie and user.cookie['session_id'].value == userCookie['session_id'].value:
            return True
        else:
            return False

    def do_HANDLE_LOGOUT(self, userWithExpiredSession: User):
        """ Function for handling q logout request.

            :param userWithExpiredSession:   The user whose about to be logged out.

                note::  Author(s): Mitch """

        self.sessionManager.removeClient(userWithExpiredSession)
        self.do_HANDLE_SUCCESSFUL_REQUEST('Logged out successfully.')

    def do_PROCESS_REGISTRATION_REQUEST(self, registration: dict):
        """ Processes the dictionary from a registration request.

            :param registration:    The dictionary from the registration request body.

                note::  Author(s): Mitch """

        if 'Keyhash' not in registration or 'User' not in registration or 'Pass' not in registration:
            self.do_HANDLE_INVALID_REQUEST(400, 'Bad Request: Registration request was incomplete.')
        else:
            if registration['Keyhash'] not in BFAUsers:
                self.do_HANDLE_INVALID_REQUEST(400, 'Bad Request: This keyhash is not eligible for registration')
            else:
                if BFAUsers[registration['Keyhash']].isRegistered():
                    self.do_HANDLE_INVALID_REQUEST(
                        400, 'Bad Request: The provided keyhash is already registered.')
                else:
                    bfaUser = BFAUsers[registration['Keyhash']]
                    bfaUser.setUser(registration['User'])
                    bfaUser.setPass(registration['Pass'])
                    self.do_HANDLE_SUCCESSFUL_REQUEST('Successful registration.')

    def do_PROCESS_LOGIN_REQUEST(self, login: dict):
        """ Processes the dictionary from a log-in request.

            :param login:   The dictionary from the log-in request body.

                note::  Author(s): Mitch """

        if 'Keyhash' not in login or 'User' not in login or 'Pass' not in login:
            self.do_HANDLE_INVALID_REQUEST(400, 'Bad Request: Log-in request was incomplete.')
        else:
            if login['Keyhash'] not in BFAUsers:
                self.do_HANDLE_INVALID_REQUEST(400, 'Bad Request: This keyhash is not eligible for log-in.')
            else:
                user = BFAUsers[login['Keyhash']]
                if not user.credentialsMatch(login['User'], login['Pass']):
                    self.do_HANDLE_INVALID_REQUEST(400, 'Bad Request: Credentials don\'t match.')
                else:
                    if user.isOnline() and not user.allowsMultipleLogins():
                        self.do_HANDLE_INVALID_REQUEST(403, 'Unauthorized Request: This is user is already logged in!'
                                                            'Multiple log-ins are not permitted for this user.')
                    else:
                        now = datetime.now(timezone.utc)
                        sessionCookie = self.createSessionCookie(now)
                        self.sessionManager.addClient(self.client_address, user, sessionCookie, now)
                        self.do_HANDLE_SUCCESSFUL_REQUEST('Success: You successfully logged in!')

    def do_HANDLE_INITIAL_PUT_REQUEST(self):
        """ Handles an initial put request. This should be a login or registration attempt if used correctly.

                note:: Author(s): Mitch """

        if self.path != '/register' and self.path != '/login':
            self.send_response(400)
            self.end_headers()
            self.do_SEND_SIMPLE_RESPONSE('Bad Request: Please register or login first!')
        else:
            if self.path == '/register':
                content_length = int(self.headers['Content-Length'])
                if content_length == 0:
                    self.do_HANDLE_INVALID_REQUEST(400, 'Missing registration information.')
                else:
                    body = self.rfile.read(content_length)
                    bodyDict = json.loads(body)
                    self.do_PROCESS_REGISTRATION_REQUEST(bodyDict)
            else:   # Implies that: self.path == '/login'
                content_length = int(self.headers['Content-Length'])
                if content_length == 0:
                    self.do_HANDLE_INVALID_REQUEST(400, 'Missing login information.')
                else:
                    body = self.rfile.read(content_length)
                    bodyDict = json.loads(body)
                    self.do_PROCESS_LOGIN_REQUEST(bodyDict)
