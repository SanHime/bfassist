#############################################################################
#
#
#   BFA SQL Module
#
#
#############################################################################
""" This module introduces a db-powered dictionary. Apart from introducing basic methods to access and interact with the
data it also offers a few more complex functions for interaction with the database.

For instance it gives the ability to add data priority rules from the db management class, find data sets via an entry
in a column with the UNIQUE constraint or by all its values except for the primary key.

    Dependencies:

        sql <- dbdictionary
         \
          -> dbmanagement   @DBDict.startSQL, @DBDict.addDataPriorityRule

        note::  Author(s): Mitch last-check: 07.07.2021 """

from threading import Lock
from os import path
from sqlite3 import Cursor, Connection, connect
from typing import get_type_hints

from bfassist.sql import DBStorable


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class DBDict:
    """ Class to simplify database interaction. Basically turning a table in the database into a python dictionary.

        :param table:               The name of the table in which data will be stored.
        :param storeType:           Class of the elements stored. Inheriting from DBStorable which will use this class
                                    for database interaction.
        :param requireLiveSet:      Flag showing if a live set should be kept for this database dictionary.

        :param column_definitions:  A dictionary containing the column definitions depending on the store type
                                    {columnName: [columnDataType, "modifiers"...]}. Taken from the store type.
        :param liveSet:             A live set containing all elements stored.
        :param primary:             Column name of the primary key.
        :param indexOfPrimary:      The index of the primary column in the list of columns.

        :param db:                  The cursor of the database.
        :param dbLock:              The threading lock for the cursor of this database.
        :param bfaSQLdatabase:      The connection to the database.

            note::  Author(s): Mitch """
    def __init__(self, table: str, storeType: DBStorable, requireLiveSet: bool = True, column_definitions: dict = None,
                 liveSet: set = None, primary: str = "", indexOfPrimary: int = None, db: Cursor = None,
                 dbLock: Lock = None, bfaSQLdatabase: Connection = None):

        if isinstance(db, Cursor) and isinstance(bfaSQLdatabase, Connection) and dbLock is not None:
            self.db = db
            self.bfaSQLdatabase = bfaSQLdatabase
        else:
            self.startSQL()
            self.dbLock = Lock()

        self.table = table
        self.storeType = storeType
        self.requireLiveSet = requireLiveSet

        if column_definitions:
            self.column_definitions = column_definitions
        else:
            self.column_definitions = self.storeType.column_definitions

        if liveSet:
            self.liveSet = liveSet
        else:
            self.liveSet = set()

        if primary:
            self.primary = primary
        else:
            for columnName in self.column_definitions:
                if 'PRIMARY KEY' in self.column_definitions[columnName][1]:
                    self.primary = columnName
            if not self.primary:
                raise ValueError('No primary key found!')

        if indexOfPrimary:
            self.indexOfPrimaryKey = indexOfPrimary
        else:
            self.indexOfPrimaryKey = list(self.column_definitions.keys()).index(self.primary)

        if self.tableExists():
            if not self.tableStructureMatch():
                self.backupTable()
                self.setup()
        else:
            self.setup()

        if self.requireLiveSet:
            self.refresh_liveSet()

    def backupTable(self):
        """ Function to backup a table. Intended for use when a table structure mismatch was detected.

                note::  Author(s): Mitch """

        varC = 1

        while self.tableExists(str(varC)):
            varC += 1

        try:
            self.dbLock.acquire(True)
            self.db.execute("ALTER TABLE " + self.table + " rename to " + self.table + str(varC))
            self.bfaSQLdatabase.commit()
            self.db.fetchall()
        finally:
            self.dbLock.release()

    def tableStructureMatch(self):
        """ Function to check if the existing table matches the currently defined structures.

            :return:    True if table structures matches, otherwise false.

                note::  Author(s): Mitch """

        try:
            self.dbLock.acquire(True)
            self.db.execute("SELECT sql FROM sqlite_master WHERE type=\'table\' AND name =\'" + self.table + "\'")
            ret = self.db.fetchone()[0]
        finally:
            self.dbLock.release()

        if ret == self.createTableString():
            return True
        else:
            return False

    def tableExists(self, suffix: str = ""):
        """ Function to check if the table exists already (a table having the appropriate name).

            :param suffix:  Suffix to add to table name for simple way of backing up tables.

            :return:        True if table exists, otherwise false.

                note::  Author(s): Mitch """

        try:
            self.dbLock.acquire(True)
            self.db.execute("SELECT count(name) FROM sqlite_master WHERE type=\'table\' AND name =\'" + self.table +
                            suffix + "\'")
            ret = self.db.fetchone()[0]
        finally:
            self.dbLock.release()

        if ret == 1:
            return True
        else:
            return False

    def startSQL(self):
        """ Function to connect to the SQL database.

            :return:    True at the end.

                note::  Author(s): Mitch """

        from bfassist.sql.dbmanagement import Management, DB_PATH

        print("Attempting to establish a connection to the database.")
        if path.exists(DB_PATH):
            self.bfaSQLdatabase = connect(DB_PATH, check_same_thread=False, timeout=5)
            self.db = self.bfaSQLdatabase.cursor()
        else:
            print("Database didn't exist, creating a new one!")
            self.bfaSQLdatabase = connect(DB_PATH, check_same_thread=False, timeout=5)
            self.db = self.bfaSQLdatabase.cursor()

        if Management.db_size is None:
            Management.updateDBSize()

        return True

    def stopSQL(self):
        """ Function to disconnect from the SQL database.

            :return:    True at the end.

                note::  Author(s): Mitch """

        if isinstance(self.bfaSQLdatabase, Connection):
            log("Closing connection to the database.")
            self.bfaSQLdatabase.close()

        return True

    def createTableString(self):
        """ Function to create the string required to create the sql table required.

            :return:    The string to create the table.

                note::  Author(s): Mitch """

        return "CREATE TABLE " + self.table + "(" + ', '.join([columnName + " " + self.column_definitions[columnName][1]
                                                               for columnName in self.column_definitions]) + ")"

    def setup(self):
        """ Sets up this table when its needed for the first time.

                note:: Author(s): Mitch """

        try:
            self.dbLock.acquire(True)
            self.db.execute(self.createTableString())
            self.bfaSQLdatabase.commit()
        finally:
            self.dbLock.release()

    def refresh_liveSet(self):
        """ Simple function to refresh the live set of this table.

            note::  Author(s): Mitch """

        ret = []
        try:
            self.dbLock.acquire(True)
            self.db.execute("SELECT * FROM " + self.table)
            ret = self.db.fetchall()
        finally:
            self.dbLock.release()
            self.liveSet = set([self[row[self.indexOfPrimaryKey]] for row in ret])

    def __iter__(self):
        """ Gets the elements as iterator.

            :return:    Iterator elements in this table.

                note::  Author(s): Mitch """

        if not self.liveSet:
            self.refresh_liveSet()

        return self.liveSet.__iter__()

    def __getitem__(self, item: str):
        """ Performs a select via primary key and returns the element.

            :param item:    The primary key for the element to return.

            :return:        The element indexed with the primary key.

                note::  Author(s): Mitch """

        for element in self.liveSet:
            # noinspection PyTypeChecker
            if isinstance(element, self.storeType) and element.getPrimaryKeyValue() == item:
                return element

        try:
            self.dbLock.acquire(True)
            self.db.execute('SELECT * FROM ' + self.table + ' WHERE ' + self.primary + '=?', (item,))
            ret = self.db.fetchall()[0]
        finally:
            self.dbLock.release()

        if ret:
            to_up = self.storeType.fromSQLResult(ret)

            if self.requireLiveSet:
                self.liveSet.add(to_up)
            return to_up
        else:
            return None

    def __setitem__(self, key: str, value: DBStorable):
        """ Performs an insert of an element into the table.

            :param key:     The value of the primary key.
            :param value:   The element to be stored in the table.

                note::  Author(s): Mitch """

        try:
            self.dbLock.acquire(True)
            self.db.execute(
                "INSERT INTO " + self.table + " VALUES (" + ("?," * len(self.column_definitions))[:-1] + ")",
                value.intoSQLTuple())
            self.bfaSQLdatabase.commit()

            if key is None:
                self.db.execute("select last_insert_rowid()")
                ret = self.db.fetchall()[0]
                key = value.sqlToPyForPy[get_type_hints(value.__init__)[value.getPrimaryKey()]](ret[0])
                value.setPrimaryKeyValue(key)

                self.db.execute("DELETE FROM " + self.table + " WHERE " + value.getPrimaryKey() +
                                " IS NULL OR trim(" + value.getPrimaryKey() + ") = '';")
                self.bfaSQLdatabase.commit()

            if self.requireLiveSet:
                self.liveSet.add(value)
        finally:
            self.dbLock.release()

    def __contains__(self, item: str):
        """ Takes a string and checks if it's a known primary key.

            :param item:    String to be checked.

            :return:        True if the key exists. False otherwise.

                note::  Author(s): Mitch """

        try:
            self.dbLock.acquire(True)
            self.db.execute("SELECT * from " + self.table + " WHERE " + self.primary + "=?", (item,))
            if self.db.fetchall():
                return True
            else:
                return False
        finally:
            self.dbLock.release()

    def remove(self, item: str):
        """ Removes an element from the table via its primary key.

            :param item:    Primary key value.

            :return:        True when complete.

                note::  Author(s): Mitch """

        try:
            self.dbLock.acquire(True)
            self.db.execute("DELETE FROM " + self.table + " WHERE " + self.primary + "=?", (item,))
            self.db.fetchall()
            self.bfaSQLdatabase.commit()
        finally:
            self.dbLock.release()
            if self.requireLiveSet:
                self.refresh_liveSet()

        if item in self:
            return False
        else:
            return True

    def fetchSingleWhere(self, field: str, item):
        """ If column has UNIQUE constraint fetch from it at secondary key.

            :param field:   The column that should function as secondary key and has to be UNIQUE.
            :param item:    The value we are looking for.

            :return:        The unique element.

                note::  Author(s): Mitch """

        if 'UNIQUE' in self.column_definitions[field][1]:
            for element in self.liveSet:
                # noinspection PyTypeChecker
                if isinstance(element, self.storeType) and element.__getattribute__('get' + field)() == item:
                    return element
            try:
                self.dbLock.acquire(True)
                self.db.execute('SELECT * FROM ' + self.table + ' WHERE ' + field + '=?', (item,))

                ret = self.db.fetchall()

                if ret:
                    ret = ret[0]
                else:
                    return None
            finally:
                self.dbLock.release()

            if ret:
                to_up = self.storeType.fromSQLResult(ret[0])

                if self.requireLiveSet:
                    self.liveSet.add(to_up)
                return to_up
            else:
                return None
        else:
            return None

    def exists(self, fd: dict):
        """ Checks if a row with the given values exists.

            :param fd:  Fully qualified definition of the row including all columns except for the primary key
                        as keys and their values respectively.

                note::  Author(s): Mitch """

        for element in self.liveSet:
            if all([True if element.__getattribute__('get' + attr)() == fd[attr] else False for attr in fd]):
                return True

        try:
            self.dbLock.acquire(True)
            self.db.execute('SELECT * FROM ' + self.table + ' WHERE ' + ' AND '.join(field + '=?' for field in fd),
                            (*fd.values(),))
            ret = self.db.fetchall()
        finally:
            self.dbLock.release()

        if ret:
            if self.requireLiveSet:
                self.liveSet.add(self.storeType.fromSQLResult(ret[0]))
            return True
        else:
            return False

    def getWithoutIdByFullDefinition(self, fd: dict):
        """ Returns a stored element without knowing its Id based on that it exists.
        If multiple such elements with differing Ids exist then it will return the one fetched first.

            :param fd:  Fully qualified definition of the row including all columns except for the primary key
                        as keys and their values respectively.

            :return:    The element defined if it exists. Otherwise None.

                note::  Author(s): Mitch """

        for element in self.liveSet:
            if all([True if element.__getattribute__('get' + attr)() == fd[attr] else False for attr in fd]):
                return element

        try:
            self.dbLock.acquire(True)
            self.db.execute('SELECT * FROM ' + self.table + ' WHERE ' + ' AND '.join(field + '=?' for field in fd),
                            (*fd.values(),))
            ret = self.db.fetchall()
        finally:
            self.dbLock.release()

        if ret:
            element = self.storeType.fromSQLResult(ret[0])
            if self.requireLiveSet:
                self.liveSet.add(element)
            return element
        else:
            return None

    def addDataPriorityRule(self, condition: str, priorityLevel: int = 0):
        """ Adds a data priority rule for this dictionary.

            :param condition:       Conditions to build the SQL command to find all such elements in the database.
            :param priorityLevel:   Integer representation of the priority level, greater means higher priority.

                note::  Author(s): Mitch """

        from bfassist.sql.dbmanagement import DBPriority

        DBPriority("FROM " + self.table + " WHERE " + condition, priorityLevel)

    def addDataPriorityRules(self, priorityRuleDefinitions: set):
        """ Adds a set of data priority rules for this dictionary.

            :param priorityRuleDefinitions: A set containing tuples with conditions and priority levels.

                note::  Author(s): Mitch """

        for rule in priorityRuleDefinitions:
            self.addDataPriorityRule(*rule)

    def getLastInsertedItem(self):
        """ Returns the db storable inserted last.

            :return:    The last inserted db storable. None if there wasn't any element inserted to this table before.

                note::  Author(s): Mitch """

        try:
            self.dbLock.acquire(True)
            self.db.execute("SELECT * FROM " + self.table + " ORDER BY ROWID DESC LIMIT 1")
            ret = self.db.fetchall()
        finally:
            self.dbLock.release()

        if ret:
            element = self.storeType.fromSQLResult(ret[0])
            if self.requireLiveSet:
                self.liveSet.add(element)
            return element
        else:
            return None
