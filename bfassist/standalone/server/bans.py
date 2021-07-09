#############################################################################
#
#
#   Ban Module to BFA v. c7
#
#
#############################################################################
""" Simple module for managing bans on a battlefield 1942 server.

    Dependencies:

        bfassist <- standalone <- (server.)bans
            \
             -> sql

        Author(s): henk, Mitch last-check: 08.07.2021 """

from datetime import datetime

from bfassist.standalone import Server
from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Ban(DBStorable, table="bans", live=False):
    """ Simple ban system to manage and keep track of bans.

        :param server:      Server the ban was issued on.

        :param BanId:       Identifier of the ban in the database.
        :param Keyhash:     Keyhash of the banned player.
        :param DateOfIssue: Datetime object of when the ban was entered to the system.
        :param Duration:    Duration of the ban.
        :param Reason:      Reason of the ban.

            note::  Author(s): Mitch, henk """

    def insertToDB(self):
        """ Overrides the insertToDB function so that ban issuance is sent from the server object.

                note::  Author(s): Mitch, henk """

        self.server.banPlayerByKeyhash(self.getKeyhash())
        super().insertToDB()

    def __init__(self, server: Server, Keyhash: str, BanId: int = None, DateOfIssue: datetime = None,
                 Duration: int = 0, Reason: str = ""):
        self.server = server

        self.SBanId = BanId, INTEGER, PRIMARY_KEY
        self.SKeyhash = Keyhash, VARCHAR(255)
        if DateOfIssue:
            self.SDateOfIssue = DateOfIssue, DATETIME
        else:
            self.SDateOfIssue = datetime.now()
        self.SDuration = Duration, INTEGER
        self.SReason = Reason, TINYTEXT

        self.insertToDB()

    @staticmethod
    def reset(server: Server):
        """ Function to clear the ban list of a server.

                note::  Author(s): henk, Mitch """

        server.writeToServer("Clearing ban list of this server.")
        server.clearBanList()

        for ban in Ban.storageDict:
            if ban.server == server:
                ban.delete()
