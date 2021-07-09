#############################################################################
#
#
#   Webclient Colour Scheme Module to BFA c7 Standalone
#
#
#############################################################################
""" This module defines the colour scheme used by the webclient.

    Dependencies:

        bfassist <- (standalone.webclient.)colourscheme
            \
             -> colours

        note::  Author(s): last-check: 08.07.2021 """

from bfassist.colours import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


BFA_COLOURS = ColourScheme("BFA Colour Scheme")

BFA_COLOURS.BLUE = RGBA_Colour('blue', 79, 169, 255, 1)
BFA_COLOURS.GREY = RGBA_Colour('grey', 0, 0, 0, 0.7)
BFA_COLOURS.GREEN = RGBA_Colour('green', 126, 187, 153, 1)
BFA_COLOURS.MIDNIGHT_BLUE = RGB_Colour('midnight-blue', 32, 37, 89)
BFA_COLOURS.RED = RGBA_Colour('red', 255, 121, 91, 1)
BFA_COLOURS.SILVER = RGB_Colour('silver', 190, 187, 187)
BFA_COLOURS.SLATE_GREY = RGB_Colour.fromHex('slate-grey', '708090')
BFA_COLOURS.DARK_GREY = RGB_Colour.fromHex('dark-grey', '292929')
BFA_COLOURS.LIGHT_GREY = RGB_Colour.fromHex('light-grey', 'eeeeee')
