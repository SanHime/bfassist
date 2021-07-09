#############################################################################
#
#
#   Colour Scheme webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a colour scheme module for bfa colours.

    Dependencies:

        colourschemes
            |
            v
        rgbcolours

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.colours.rgbcolours import RGBA_Colour, RGB_Colour, Colour


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ColourScheme:
    """ Representation of a colour scheme/palette.

        :param name:            Name of this colour scheme.
        :param colours:         Dictionary holding the colors of this scheme,
                                colour names as anchors and rgba as values.

        #   Easy access colour properties.
        :param BLUE:            Blue of this scheme.
        :param GREY:            Grey of this scheme.
        :param GREEN:           Green of this scheme.
        :param MIDNIGHT_BLUE:   Midnight-blue of this scheme.
        :param RED:             Red of this scheme.
        :param SILVER:          Silver of this scheme.
        :param SLATE_GREY:      Slat-grey of this scheme.
        :param DARK_GREY:       Dark-grey of this scheme.
        :param LIGHT_GREY:      Light-grey of this scheme.

            note::  Author(s): Mitch """

    def __init__(self, name: str, colours: dict = None, BLUE: Colour = None, GREY: Colour = None,
                 GREEN: Colour = None, MIDNIGHT_BLUE: Colour = None, RED: Colour = None,  SILVER: Colour = None,
                 SLATE_GREY: Colour = None, DARK_GREY: Colour = None, LIGHT_GREY: Colour = None):

        self.name = name

        if colours is None:
            self.colours = {}
        else:
            self.colours = colours

        if 'BLUE' in self.colours:
            self.BLUE = self.colours['BLUE']
        else:
            self.BLUE = BLUE

        if 'GREY' in self.colours:
            self.GREY = self.colours['GREY']
        else:
            self.GREY = GREY

        if 'GREEN' in self.colours:
            self.GREEN = self.colours['GREEN']
        else:
            self.GREEN = GREEN

        if 'MIDNIGHT_BLUE' in self.colours:
            self.MIDNIGHT_BLUE = self.colours['MIDNIGHT_BLUE']
        else:
            self.MIDNIGHT_BLUE = MIDNIGHT_BLUE

        if 'RED' in self.colours:
            self.RED = self.colours['RED']
        else:
            self.RED = RED

        if 'SILVER' in self.colours:
            self.SILVER = self.colours['SILVER']
        else:
            self.SILVER = SILVER

        if 'SLATE_GREY' in self.colours:
            self.SLATE_GREY = self.colours['SLATE_GREY']
        else:
            self.SLATE_GREY = SLATE_GREY

        if 'DARK_GREY' in self.colours:
            self.DARK_GREY = self.colours['DARK_GREY']
        else:
            self.DARK_GREY = DARK_GREY

        if 'LIGHT_GREY' in self.colours:
            self.LIGHT_GREY = self.colours['LIGHT_GREY']
        else:
            self.LIGHT_GREY = LIGHT_GREY

    @property
    def BLUE(self):
        return self._BLUE

    @BLUE.setter
    def BLUE(self, colour: Colour):
        self._BLUE = colour
        self.colours['BLUE'] = colour

    @property
    def GREY(self):
        return self._GREY

    @GREY.setter
    def GREY(self, colour: Colour):
        self._GREY = colour
        self.colours['GREY'] = colour

    @property
    def GREEN(self):
        return self._GREEN

    @GREEN.setter
    def GREEN(self, colour: Colour):
        self._GREEN = colour
        self.colours['GREEN'] = colour

    @property
    def MIDNIGHT_BLUE(self):
        return self._MIDNIGHT_BLUE

    @MIDNIGHT_BLUE.setter
    def MIDNIGHT_BLUE(self, colour: Colour):
        self._MIDNIGHT_BLUE = colour
        self.colours['MIDNIGHT_BLUE'] = colour

    @property
    def RED(self):
        return self._RED

    @RED.setter
    def RED(self, colour: Colour):
        self._RED = colour
        self.colours['RED'] = colour

    @property
    def SILVER(self):
        return self._SILVER

    @SILVER.setter
    def SILVER(self, colour: Colour):
        self._SILVER = colour
        self.colours['SILVER'] = colour

    @property
    def SLATE_GREY(self):
        return self._SLATE_GREY

    @SLATE_GREY.setter
    def SLATE_GREY(self, colour: Colour):
        self._SLATE_GREY = colour
        self.colours['SLATE_GREY'] = colour

    @property
    def DARK_GREY(self):
        return self._DARK_GREY

    @DARK_GREY.setter
    def DARK_GREY(self, colour: Colour):
        self._DARK_GREY = colour
        self.colours['DARK_GREY'] = colour

    @property
    def LIGHT_GREY(self):
        return self._LIGHT_GREY

    @LIGHT_GREY.setter
    def LIGHT_GREY(self, colour: Colour):
        self._LIGHT_GREY = colour
        self.colours['LIGHT_GREY'] = colour
