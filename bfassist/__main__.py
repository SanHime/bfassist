#############################################################################
#
#
#   BF-Assist c7-branch Main module
#
#
#############################################################################
""" Main module of bfa.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 08.07.2021 """

from sys import path
path += ['.']   # Required to make absolute imports work as they usually do

from bfassist import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


startup()
main()
