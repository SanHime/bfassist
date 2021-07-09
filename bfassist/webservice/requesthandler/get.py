#############################################################################
#
#
#   Webservice GET Request Handling for BFA
#
#
#############################################################################
""" This provides the request handling of GET requests.

    Dependencies:

        requesthandler <- get
            \
             -> sessionmanagement

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webservice.requesthandler import AuthenticationRequestHandler
from bfassist.webservice.requesthandler.sessionmanagement import User


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class GET_RequestHandler(AuthenticationRequestHandler):
    """ The GET request handler.

            note::  Author(s): Mitch """

    VIEWS = {}

    def do_GET(self):
        """ Handles HTTP-GET requests.

                note::  Author(s): Mitch """

        user = self.getUser()
        if user is None:
            self.do_HANDLE_UNAUTHORIZED_GET_REQUEST()
        else:
            if self.isValidSessionOf(user):
                self.do_GET_ON_VALID_SESSION(user)
            else:
                self.do_HANDLE_EXPIRED_SESSION(user)

    def do_HANDLE_UNAUTHORIZED_GET_REQUEST(self):
        """ To be overridden. Function for handling an unauthorized GET request to possible serve some View even without
        being authenticated (login view for instance).

                note::  Author(s): Mitch """

        pass

    def do_PROCESS_POTENTIAL_API_GET_REQUEST(self, issuingUser: User):
        """ To be overridden. Function for extracting parameters and function of the API to be called and checking if
        they are valid.

            :param issuingUser: The user issuing the GET request.

                note::  Author(s): Mitch """

        pass

    def do_GET_ON_VALID_SESSION(self, issuingUser: User):
        """ Could be overridden if wanting to make use of the issuingUser for choking/customizing access.

            :param issuingUser: The user issuing the GET request.

                note::  Author(s): Mitch """

        potentialViewName = self.path.split('/')[1]

        if potentialViewName == 'favicon.ico':
            self.do_PREPARE_STANDARD_WEBSITE_HEADERS()
            self.do_REPLY_WITH_VIEW(None, issuingUser)
        elif potentialViewName in self.Views:
            self.do_PREPARE_STANDARD_WEBSITE_HEADERS()
            self.do_REPLY_WITH_VIEW(self.Views[potentialViewName], issuingUser)
        else:
            self.do_PROCESS_POTENTIAL_API_GET_REQUEST(issuingUser)
