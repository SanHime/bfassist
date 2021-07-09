#############################################################################
#
#
#   Colour module to BFA c7
#
#
#############################################################################
""" This is a very simplistic colour module for managing rgb/a colours and define colour schemes with them. This module
provides only what's necessary for bfa up to this point. I will consider to replace this module with something better
that already exists. However, slowly expanding this would probably be easy and therefore is also a reasonable
possibility.

    Dependencies:

        colours ---\-> rgbcolours
                    -> colourschemes

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.colours.rgbcolours import Colour, RGB_Colour, RGBA_Colour
from bfassist.colours.colourschemes import ColourScheme


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass
