#############################################################################
#
#
#   BFA SQL Module
#
#
#############################################################################
""" This module centralises SQL database interaction for bfa.

DBStorable is the base data type introduced with this module. A DBStorable essentially equals a dataset that can be
stored in the underlying database. Other classes that contain information that should be stored in the database can
inherit from DBStorable to save their attributes seamlessly in the database.

For instance the Player class inherits from DBStorable to save information about player objects in the database.
At inheritance one also specifies the name of the table and whether a live copy of all elements that have been inserted
to the table should be kept available in a set.

class Player(DBStorable, table="players", live=False)

Attributes that contain data that should be saved in the database are called 'S'-attributes and are signified by a
capital 'S' at the start of their name. They are assigned a tuple containing the respective value in the first position
of the tuple, the sql data type to use in the second position and any further modifiers or constraints such as UNIQUE
or PRIMARY KEY in the following positions. Consequentially 'usual' attributes of classes that inherit from DBStorable
can't start with a capital 'S' unless they are assigned using 'super().__setattr__()'. Example for an 'S'-attribute:

SId = Id, INTEGER, PRIMARY_KEY

The available data types and modifiers are defined in the dbstorable module but can be imported from this module for
convenience.

The DBDict data type is a dictionary like object that enables access and interaction with data sets in the database.
Every subclass of DBStorable automatically comes with a corresponding DBDictionary attribute that is called storageDict.

Player.storageDict

Lastly the DBManagement class is used to manage the database in its entirety. For now this is mainly focused on limiting
the total size occupied by the database. The class is instantiated once in its respective module and utilises so called
DBPriorities to attribute an integer priority to a selection of data in the database specified by a SELECT statement.
When the database surpasses a size limit specified in the dbmanagement module it is going to "condense"/delete data
specified by the priority rules starting with the lowest priority until the database size is below the limit again.
One should keep in mind that if data from a db dictionary with a live set is deleted the data will still remain in the
live set. However, db dictionaries with live sets really should not have any priority rules assigned.

If a table with the specified name exists already and does not match the current description then the old table will be
renamed and a new table will be created that matches the new specifications. A possible migration of the data from an
old table would have to be done manually. Keep in mind that this also means you shouldn't have two different tables
using the same name, although that should hopefully be obvious.

    Dependencies:

        sql ----\-> dbstorable
                 -> dbdictionary

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.sql.dbstorable import *
from bfassist.sql.dbdictionary import DBDict


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass
