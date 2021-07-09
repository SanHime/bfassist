#############################################################################
#
#
# Module of BFA that manages logging
#
#
#############################################################################
""" An extremely simple logging module that logs to the database.

    Dependencies:

        bfassist <- bfa_logging
            \
             -> sql

        note::  Author(s): Mitch last-check: 07.07.2021 """

from traceback import format_stack
from datetime import datetime

from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


logLevels = {
    0: "verbose",
    1: "info",
    2: "debug",
    3: "error",
    4: "critical",
    5: "fatal",
    "verbose": 0,
    "info": 1,
    "debug": 2,
    "error": 3,
    "critical": 4,
    "fatal": 5
}

activeLevels = {
    0: False,
    1: True,
    2: True,
    3: True,
    4: True,
    5: True
}

logSema = False


def now():
    """ Simple function to return the current time formatted as used here in bfa logging.

        :return:    String containing the current time stamp.

            note::  Author(s): Mitch """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def isActive(level: int):
    """ Simple function to check if a logging level is active.

        :return:    True if active and false otherwise.

            note::  Author(s): Mitch """

    return activeLevels[level]


def logString(message: str, level):
    """ Simple function that builds part of the logged string without the stacktrace.

        :param message:     The message to be printed and logged.
        :param level:       The log level the message is to be logged at.

        :return:            Part of a log string that looks somewhat like this [LOGLEVEL] 2021-01-01 12:00:00   :   ...

            note::  Author(s): Mitch """

    return "[" + logLevels[level].upper() + "]\t" + now() + "\t:\t" + str(message)


class LogEntry(DBStorable, table='logging', live=False):
    """ Class for managing log entries with the database. Also writes the log entry to the console when instantiated.

        :param Id:          Identifier of this log in the database.
        :param LogTime:     Datetime timestamp of the log event.
        :param Loglevel:    The log level of this entry.
        :param CodeStack:   Stack of code of this particular entry.
        :param Message:     Message inside the entry.


            note::  Author(s): Mitch """

    def __init__(self, LogLevel: int, CodeStack: str, Message: str, Id: int = None, LogTime: datetime = None):

        if LogLevel is None:
            LogLevel = 2

        print("Logger" + logString(Message, LogLevel))

        self.SId = Id, INTEGER, PRIMARY_KEY
        self.SLogTime = LogTime, DATETIME
        self.SLogLevel = LogLevel, TINYINT
        self.SCodeStack = CodeStack, TEXT
        self.SMessage = str(Message), TEXT

        self.insertToDB()


LogEntry.storageDict.addDataPriorityRules({
    ("LogLevel < 3", 0),
    ('LogTime < datetime(\'now\', \'-3 month\')', 1)
})


def log(message: str, level: int = 2, codeStack: str = ""):
    """ This function prints the logged message to the console and is supposed
    to create an entry in the respective log level.

        :param message:     The message to be printed and logged.
        :param level:       The log level the message is to be logged at.
        :param codeStack:   Should contain a string of the fully qualified function calling.

            note::  Author(s): Mitch """

    if codeStack == "":
        codeStack = "\n".join(format_stack(limit=5))

    if isActive(level):
        LogEntry(level, codeStack, message)
    else:
        return False


print("BFA-Logging enabled.")
