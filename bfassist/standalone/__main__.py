#############################################################################
#
#
#   BF-Assist Standalone c7-branch Main module
#
#
#############################################################################
""" Main module of bfa standalone.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 08.07.2021 """


from bfassist.standalone import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


KERN.run()
