#############################################################################
#
#
#   Webservice POST Request Handling for BFA
#
#
#############################################################################
""" This provides the request handling of POST requests.

    Dependencies:

        requesthandler <- post
            \
             -> sessionmanagement

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webservice.requesthandler import GET_RequestHandler
from bfassist.webservice.requesthandler.sessionmanagement import User


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class POST_RequestHandler(GET_RequestHandler):
    """ The PUT request handler.

            note::  Author(s): Mitch """

    def do_POST(self):
        """ Handles HTTP-POST requests.

                note::  Author(s): Mitch """

        user = self.getUser()
        if user is None:
            self.do_HANDLE_INVALID_REQUEST(403, 'Bad Request: Please register or log-in first.')
        else:
            if self.isValidSessionOf(user):
                self.do_POST_ON_VALID_SESSION(user)
            else:
                self.do_HANDLE_EXPIRED_SESSION(user)

    def do_PROCESS_POTENTIAL_API_POST_REQUEST(self, issuingUser: User):
        """ To be overridden. Function for extracting parameters and function of the API to be called and checking if
        they are valid.

            :param issuingUser: The user issuing the GET request.

                note::  Author(s): Mitch """

        pass

    def do_POST_ON_VALID_SESSION(self, issuingUser: User):
        """ Could be overridden if wanting to make use of the issuingUser for choking/customizing access.

            :param issuingUser: The user issuing the POST request.

                note::  Author(s): Mitch """
        self.do_PROCESS_POTENTIAL_API_POST_REQUEST(issuingUser)
