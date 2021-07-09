#############################################################################
#
#
#   BFA SQL Module
#
#
#############################################################################
""" This module introduces a SQL database storeable data type for usage with a dbdictionary. Importantly the most common
sql data types and modifiers are defined here.

    Dependencies:

        sql <- dbstorable
         |
         \-> dbdictionary   @DBStorable.__init_subclass__
          -> dbmanagement   @DBStorable.insertToDB

        note::  Author(s): Mitch last-check: 07.07.2021 """

from datetime import datetime
from typing import Union, get_type_hints


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def identity(inValue):
    return inValue


def sqlDatetimeToPy(sql: str):
    return None if sql is None else datetime.strptime(sql, '%Y-%m-%d %H:%M:%S.%f')


def sqlSetToPy(sql: str):
    """ Simple function for converting a custom sql string set to a python set using ';' as separator and '\&r01' as
    escape if the separator was contained.

        :param sql: The sql string.

        :return:    The python set.

            note::  Author(s): Mitch """

    return set([x.replace('\\&r01', ';') if x is not None else '' for x in sql.split(';')])


def sqlStrToPy(sql: str):
    return str(sql)


def sqlIntToPy(sql: str):
    return int(sql)


def sqlBoolToPy(sql: str):
    return bool(sql)


def pySetToSQL(inSet: set):
    """ Simple function for converting a python set to a database insertable string using ';' as separator and '\&r01'
    as escape if the separator is contained.

        :param inSet:   The set to insert to the database.

        :return:        The string for insertion to the database.

            note::  Author(s): Mitch """

    return ";".join([x.replace(';', '\\&r01') if x is not None else '' for x in inSet])


def pyBoolToSQL(inBool: bool):
    """ Simple function for converting a python bool to a database insertable integer(bit).

        :param inBool:  The bool to insert to the database.

        :return:        The integer(bit) to insert to the database.

            note::  Author(s): Mitch """
    if inBool:
        return 1
    else:
        return 0


BIT = 'BIT'
DATETIME = 'DATETIME'
INT = 'INT'
INTEGER = 'INTEGER'
MEDIUMINT = 'MEDIUMINT'
MEDIUMTEXT = 'MEDIUMTEXT'
SMALLINT = 'SMALLINT'
TEXT = 'TEXT'
TINYINT = 'TINYINT'
TINYTEXT = 'TINYTEXT'

PRIMARY_KEY = 'PRIMARY KEY'
UNIQUE = 'UNIQUE'


def VARCHAR(count: int = 255): return 'VARCHAR(' + str(count) + ')'


class DBStorable:
    """ Super class for objects that hold information that should be storable within the database. When inheriting the
    additional parameters 'table' and 'live' have to be passed to determine the name of the table in the database which
    the data will occupy and if a live set of all primary key values of objects that have been inserted to the database
    should be kept available to enable faster containment checks. Attributes to be stored in the database need to start
    with a capital 'S' e.g. 'SId' so they corresponding column name in the table will be called 'Id'. Furthermore
    the assigned value should be a tuple containing the actual value in the database and as second element the
    respective sql data type to use for the column.

        :param sqlToPyForPy:        A dictionary that maps types or unions of types on conversion functions that convert
                                    sql text responses to the respective python type.
        :param pyToSQL:             The inverse dictionary of sqlToPyForPy that contains the respective inverse function
                                    to convert a python type to its respective sql insertable format.

        :param table:               Name of the table the datasets will reside in.

        :param column_definitions:  A dictionary that's containing the column names as keys so the attributes declared
                                    with a capital 'S'. And as values the respective tuple of sql datatype and sql
                                    modifiers/constraints such as UNIQUE or PRIMARY KEY for that column.
        :param initialised:         A flag that determines if the column_definitions for this type have been initialised
                                    before so that we don't always have to check if an 'S'-attribute was already
                                    defined. Theoretically it's possible to set this back to False to introduce more
                                    'S'-attributes at runtime but obviously that would start a new table.
        :param column_count:        The number of columns in this table. Also the number of 'S'-attributes obviously.
        :param storageDict:         The corresponding dbdictionary that's supposed to simplify the access of the stored
                                    data.

            note::  Author(s): Mitch """

    sqlToPyForPy = {str: sqlStrToPy,
                    Union[str, None]: sqlStrToPy,
                    int: sqlIntToPy,
                    Union[int, None]: sqlIntToPy,
                    datetime: sqlDatetimeToPy,
                    Union[datetime, None]: sqlDatetimeToPy,
                    set: sqlSetToPy,
                    Union[set, None]: sqlSetToPy,
                    bool: sqlBoolToPy,
                    Union[bool, None]: sqlBoolToPy}

    pyToSQL = {str: identity,
               Union[str, None]: identity,
               int: identity,
               Union[int, None]: identity,
               datetime: identity,
               Union[datetime, None]: identity,
               set: pySetToSQL,
               Union[set, None]: pySetToSQL,
               bool: pyBoolToSQL,
               Union[bool, None]: pyBoolToSQL}

    @classmethod
    def addConversion(cls, func: callable, inverse: callable):
        """ Function for adding a conversion function and its inverse required for this DBStorable.

            :param func:        The conversion function to add.
            :param inverse: The inverse conversion function.

                note::  Author(s): Mitch """

        conversionType = get_type_hints(func).popitem()[1]
        cls.pyToSQL[conversionType] = func
        cls.pyToSQL[Union[conversionType, None]] = func
        cls.sqlToPyForPy[conversionType] = inverse
        cls.sqlToPyForPy[Union[conversionType, None]] = inverse

    @classmethod
    def addConversions(cls, *funcs: tuple):
        """ Function for adding multiple conversion functions and their inverse required for this DBStorable.

            :param funcs:    Tuples containing the conversion functions and their inverse.

                note::  Author(s): Mitch """

        for funcPair in funcs:
            cls.addConversion(*funcPair)

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, table: str, live: bool):
        """ This function is called whenever a subclass definition is finished. It sets up SQL connection and schemata
        required depending on the subclass definition.

        This function can be overridden if a dbstorable has a subclass. Keep in mind however that in that case you
        cannot keep a live set of this dbstorable.

            :param table:   The name of the table for this subclass in the database.
            :param live:    Boolean flag that indicates if a live copy of the dbdict should be kept.

                note::  Author(s): Mitch """

        from bfassist.sql import DBDict

        super().__init_subclass__()

        cls.column_definitions = {}
        cls.table = table
        cls.storageDict = {}
        cls.initialised = False

        # The next line will initialise a "fake" empty object so the column_definitions get filled which is required for
        # the creation of the dbdictionary object
        # noinspection PyArgumentList
        cls(*[None] * len(get_type_hints(cls.__init__)))

        cls.initialised = True

        cls.column_count = len(cls.column_definitions.keys())

        cls.storageDict = DBDict(table, cls, live)

    def insertToDB(self):
        """ Simple function for inserting an instance to the storage dict.

                note::  Author(s): Mitch """

        from bfassist.sql.dbmanagement import Management

        # The first condition checks that the primary key value of this object does not already exist
        # and the second condition checks that not all values evaluate to False (it's the "fake" empty object)
        if self.getPrimaryKeyValue() not in self.__class__.storageDict and\
                any(self.__getattribute__('get' + S_att)() for S_att in self.column_definitions):
            self.__class__.storageDict[self.getPrimaryKeyValue()] = self
            Management.updateDBSize()

    @classmethod
    def fromSQLResult(cls, sql: tuple):
        """ Init from SQL result.

            :param sql: The result to convert from.

                note::  Author(s): Mitch """

        args = {}
        index = 0
        for S_att in cls.__getattribute__(cls, 'column_definitions'):
            arg = sql[index]
            args[S_att] = cls.sqlToPyForPy[cls.__getattribute__(cls, 'column_definitions')[S_att][0]](arg)
            index += 1

        rArgs = []

        index = 0
        for S_att in get_type_hints(cls.__init__):
            if index == cls.column_count:
                break
            rArgs.append(args[S_att])
            index += 1

        currentClass = cls
        subclasses = currentClass.__subclasses__()
        while subclasses:
            if len(subclasses) > 1:
                raise ValueError("A DBStorable can only be subclassed once but " + str(type(currentClass)) + " has " +
                                 str(len(subclasses)) + " subclasses.")
            else:
                currentClass = subclasses[0]
                subclasses = currentClass.__subclasses__()
        return currentClass(*rArgs)

    def intoSQLTuple(self):
        """ Turns object into tuple for insertion to the database.

                note::  Author(s): Mitch """

        ret = []

        for S_att in self.column_definitions:
            ret.append(self.pyToSQL[self.column_definitions[S_att][0]](self.__getattribute__('get' + S_att)()))

        return tuple(ret)

    def getPrimaryKey(self):
        """ Returns the column name of the primary key in this table.

                note::  Author(s): Mitch """

        for S_att in self.__class__.column_definitions:
            if 'PRIMARY KEY' in self.__class__.column_definitions[S_att][1]:
                return S_att

    def getPrimaryKeyValue(self):
        """ Returns the value of what's the primary key for this object.

                note::  Author(s): Mitch """

        for S_att in self.__class__.column_definitions:
            if 'PRIMARY KEY' in self.__class__.column_definitions[S_att][1]:
                return self.__getattribute__('get' + S_att)()

    def setPrimaryKeyValue(self, key):
        """ Sets the value of what's the primary key for this object inside the database (without db interaction)
        mainly used for when an object is initialised without a defined primary key value.

            :param key: The value to be set as primary key value.

                note::  Author(s): Mitch """

        super().__setattr__('__' + self.getPrimaryKey(), key)

    def __setattr__(self, key: str, value, getOriginal: bool = False):
        """ Overriding the standard function to automatically generate getters and setters for database interaction.
        This introduces the 'S'-attributes.

            :param key:     Attribute name which will also correspond to a column name.
            :param value:   Value of the attribute.

                note::  Author(s): Mitch """

        if getOriginal:
            super().__setattr__(key, value)
        else:
            if key[0] == 'S':

                if not self.initialised:
                    self.column_definitions.__setitem__(key[1:], (get_type_hints(self.__init__)[key[1:]],
                                                                  ' '.join(value[1:])))

                super().__setattr__('__' + key[1:], value[0])

                def getValue():
                    """ Getter for 'S'-attribute-values stored in the database.

                            note::  Author(s): Mitch """
                    return self.__getattribute__('__' + key[1:])

                super().__setattr__('get' + key[1:], getValue)

                def setValue(inValue: type(value[0])):
                    """ Setter for 'S'-attribute-values stored in the database.

                            note::  Author(s): Mitch """
                    try:
                        self.storageDict.dbLock.acquire(True)
                        self.storageDict.db.execute("UPDATE " + self.table + " SET " + key[1:] + "=? WHERE " +
                                                    self.getPrimaryKey() + "=?",
                                                    (self.pyToSQL[type(inValue)](inValue), self.getPrimaryKeyValue(),))
                        self.storageDict.bfaSQLdatabase.commit()
                    finally:
                        self.storageDict.dbLock.release()
                    self.__setattr__('__' + key[1:], inValue)
                    return True

                super().__setattr__('set' + key[1:], setValue)
            else:
                super().__setattr__(key, value)

    def delete(self):
        """ Function for the deletion of this instance.

                note::  Author(s): Mitch """

        self.storageDict.remove(self.getPrimaryKeyValue())
