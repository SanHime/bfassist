#############################################################################
#
#
#   Webclient Fonts Module to BFA c7 Standalone
#
#
#############################################################################
""" This module simply makes fonts used in the webclient available by assigning their string name to a variable.

    Dependencies:

        None

        note::  Author(s): last-check: 08.07.2021 """


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


Agency_FB = "\"Agency FB\""
Sans_Serif = "sans-serif"

STANDARD_BACKUP_FONTS = [Sans_Serif]
