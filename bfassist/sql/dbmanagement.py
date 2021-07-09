#############################################################################
#
#
#   BFA SQL Module
#
#
#############################################################################
""" This module introduces a management system for the database. It holds the path to the database file and specifies
a size limit for the database which is by default 1024 ** 3 bytes i.e. 1 GB. For that it uses a dictionary of
DBPriorities that combines an integer priority with a list of data selections.

When the size of the database breaches the specified limit the management will delete data with increasing priority
until the database is below the size limit again. If no more data can be deleted an error will be raised.

    Description:

        sql <- dbmanagement

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from os import path, mkdir

from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


DB_PATH = "bfassist/sql/bfa.db"


class DBManagement:
    """ A class for managing a database in particular the size of it for now by using data priority rules and setting
    a maximum database size limit.

        :param DB_PATH:         The path to the database.
        :param DB_SIZE_LIMIT:   The maximum allowed size of the database.
        :param db_size:         Current size of the database.
        :param db_priorities:   Dictionary of integer priority keys and their priority rules as list of values.

            note::  Author(s): Mitch """

    # noinspection PyShadowingNames
    def __init__(self, DB_PATH: str = "", DB_SIZE_LIMIT: int = 1024 ** 3, db_size: int = None,
                 db_priorities: dict = None):
        self.DB_PATH = DB_PATH
        self.DB_SIZE_LIMIT = DB_SIZE_LIMIT
        self.db_size = db_size

        if db_priorities:
            self.db_priorities = db_priorities
        else:
            self.db_priorities = {}

    def addPriority(self, priority_rule: DBPriority, priority: int = 0):
        """ Simple function to add a priority to the db_priorities dictionary.

            :param priority_rule:   The priority rule.
            :param priority:        The integer priority level of the corresponding rule.

                note::  Author(s): Mitch """

        if priority not in self.db_priorities:
            self.db_priorities[priority] = [priority_rule]
        else:
            self.db_priorities[priority].append(priority_rule)

    def updateDBSize(self):
        """ Simple function to update the db_size variable that measures the size of the database file in bytes.

                note::  Author(s): Mitch """

        self.db_size = path.getsize(self.DB_PATH)

        while self.db_size > self.DB_SIZE_LIMIT:
            if not self.condenseDB(self.db_size - self.DB_SIZE_LIMIT):
                print("CRITICAL ERROR: RUNNING OUT OF DATABASE SPACE AND CAN'T CONDENSE ANY FURTHER\n"
                      "PLEASE BACKUP THE DATABASE AND RESET IT OR INCREASE THE SIZE LIMIT MANUALLY")

    def condenseDB(self, reduce_by: int):
        """ Function to condense the database size hopefully at least reduce_by number of bytes.

            :param reduce_by:   Size in bytes that the database should be reduced to.

                note::  Author(s): Mitch """

        for priority in sorted(self.db_priorities.keys()):
            for current_priority_rule in self.db_priorities[priority]:
                if isinstance(current_priority_rule, DBPriority) and current_priority_rule.countNumberOfElements() > 0:
                    self.updateDBSize()
                    db_size_before = self.db_size
                    eCount = current_priority_rule.deleteAllElements()[0]
                    self.updateDBSize()
                    deletedVolume = db_size_before - self.db_size
                    current_priority_rule.setApproximateElementSize(deletedVolume // eCount)
                    reduce_by -= deletedVolume
                if reduce_by < 0:
                    return True

        return False


Management = DBManagement(DB_PATH)


class DBPriority(DBStorable, table="priorityrules", live=False):
    """ Class that defines a data priority rule for the automatic deletion of low priority and non-critical data.

        :param LocationRule:            SQL command to find all such elements in the database.
                                        (Also serves as primary key.)
        :param PriorityLevel:           Integer representation of the priority level, greater means higher priority.
        :param ApproxNumberOfElements:  Number of elements in the database with this priority rule.
        :param ApproximateElementSize:  Approximate size that's freed upon deletion of a single element.

            note::  Author(s): Mitch """

    def __init__(self, LocationRule: str = None, PriorityLevel: int = 0, ApproxNumberOfElements: int = 0,
                 ApproximateElementSize: int = None):

        self.SLocationRule = LocationRule, TEXT, PRIMARY_KEY
        self.SPriorityLevel = PriorityLevel, INTEGER
        self.SApproxNumberOfElements = ApproxNumberOfElements, INTEGER
        self.SApproximateElementSize = ApproximateElementSize, INTEGER

        self.insertToDB()

    def countNumberOfElements(self):
        """ Simple function to count and update the number of elements that belong to this priority rule.

                note::  Author(s): Mitch """

        try:
            self.storageDict.dbLock.acquire(True)
            self.storageDict.db.execute("SELECT COUNT(*) " + self.getLocationRule())
            ret = self.storageDict.db.fetchall()[0]
            self.storageDict.bfaSQLdatabase.commit()
        finally:
            self.storageDict.dbLock.release()

        self.setApproxNumberOfElements(ret)

        return ret

    def deleteAllElements(self):
        """ Function that executes the SQL deletion rule for removing all elements associated with this priority rule.

            :return:    The approximate number of bytes freed up from the deletion.

                note::  Author(s): Mitch """

        eCount = self.getApproxNumberOfElements()
        if self.getApproximateElementSize() is None:
            approx_size = eCount
        else:
            approx_size = self.getApproxNumberOfElements() * self.getApproximateElementSize()
        try:
            self.storageDict.dbLock.acquire(True)
            self.storageDict.db.execute("DELETE " + self.getLocationRule())
            self.storageDict.db.fetchall()
            self.storageDict.bfaSQLdatabase.commit()
        finally:
            self.storageDict.dbLock.release()

        self.setNumberOfElements(0)

        return eCount, approx_size


PriorityRules = DBPriority.storageDict
