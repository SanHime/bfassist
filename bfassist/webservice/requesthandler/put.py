#############################################################################
#
#
#   Webservice PUT Request Handling for BFA
#
#
#############################################################################
""" This provides the request handling of PUT requests.

    Dependencies:

        requesthandler <- put
            \
             -> sessionmanagement

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webservice.requesthandler import POST_RequestHandler
from bfassist.webservice.requesthandler.sessionmanagement import User


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class PUT_RequestHandler(POST_RequestHandler):
    """ The PUT request handler.

            note::  Author(s): Mitch """

    def do_PUT(self):
        """ Handles HTTP-PUT requests. This includes login!

                note::  Author(s): Mitch """

        user = self.getUser()
        if user is None:
            self.do_HANDLE_INITIAL_PUT_REQUEST()
        else:
            if self.isValidSessionOf(user):
                self.do_PUT_ON_VALID_SESSION(user)
            else:
                if self.path == '/register' or self.path == '/login':
                    self.do_HANDLE_LOGOUT(user)
                    self.do_HANDLE_INITIAL_PUT_REQUEST(user)
                else:
                    self.do_HANDLE_EXPIRED_SESSION(user)

    def do_PROCESS_POTENTIAL_API_PUT_REQUEST(self, issuingUser: User):
        """ To be overridden. Function for extracting parameters and function of the API to be called and checking if
        they are valid.

            :param issuingUser: The user issuing the PUT request.

                note::  Author(s): Mitch """

        pass

    def do_PUT_ON_VALID_SESSION(self, issuingUser: User):
        """ Could be overridden if wanting to make use of the issuingUser for choking/customizing access.

            :param issuingUser: The user issuing the PUT request.

                note::  Author(s): Mitch """

        if self.path == '/logout':
            self.do_HANDLE_LOGOUT()
        else:
            self.do_PROCESS_POTENTIAL_API_PUT_REQUEST(issuingUser)
