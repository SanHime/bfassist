#############################################################################
#
#
#   Main Module to BFA c7 Master
#
#
#############################################################################
""" Main module of bfa master.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.master import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


main()
