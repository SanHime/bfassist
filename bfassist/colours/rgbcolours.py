#############################################################################
#
#
#   RGB/A Colour webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a rgb/a colour module for bfa colours.

Dependencies:

    None

        note::  Author(s): Mitch last-check: 07.07.2021 """


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Colour:
    """ Base class for representing any colour.

        :param name:    Name of this colour.

            note::  Author(s): Mitch """

    def __init__(self, name):
        self.name = name

    def toCSS(self):
        """ To be overridden. """

        pass


class RGB_Colour(Colour):
    """ Represents a colour in rgb encoding.

        :param name:    Name of this colour.
        :param red:     Red value of this colour.
        :param green:   Green value of this colour.
        :param blue:    Blue value of this colour.

            note::  Author(s): Mitch """

    def __init__(self, name: str, red: int, green: int, blue: int):
        super().__init__(name)
        self.red = red
        self.green = green
        self.blue = blue

    def toCSS(self):
        """ Converts the colour to a CSS readable string.

            :return:    CSS string.

                note::  Author(s): Mitch """

        return "rgb(" + ",".join([str(self.red), str(self.green), str(self.blue)]) + ")"

    @classmethod
    def fromHex(cls, name: str, hexString: str):
        """ Alternative constructor to instantiate a colour via its hex-string definition.

            :param name:        Name of the colour
            :param hexString:   The hex-string containing the rgb values of the colour.

            :return:            The rgb colour corresponding to the hex-string.

                note::  Author(s): Mitch """

        return cls(name, int(hexString[:2], 16), int(hexString[2:4], 16), int(hexString[4:], 16))


class RGBA_Colour(RGB_Colour):
    """ Represents a colour in rgba encoding.

        :param name:    Name of this colour.
        :param alpha:   Alpha(opacity) value of this colour.

            note::  Author(s): Mitch """

    def __init__(self, name: str, red: int, green: int, blue: int, alpha: float):
        super().__init__(name, red, green, blue)
        self.alpha = alpha

    def toCSS(self):
        """ Converts the colour to a CSS readable string.

            :return:    CSS string.

                note::  Author(s): Mitch """

        return "rgba(" + ",".join([str(self.red), str(self.green), str(self.blue), str("%.2f" % self.alpha)]) + ")"

    def toRGB(self):
        """ Converts the RGBA colour to an RGB colour.

            :return:    RGB colour disregarding the alpha value.

                note::  Author(s): Mitch """

        return RGB_Colour(self.name, self.red, self.green, self.blue)

    def createVariant(self, variation: str):
        """ Creates a variant of this colour.

            :param variation:   The type of variation that's desired.

            :return:            RGBA colour variation if applicable, otherwise None.

                note::  Author(s): Mitch """

        if variation == 'faint':
            if self.alpha > 0.21:
                return RGBA_Colour(variation + self.name, self.red, self.green, self.blue, self.alpha-0.21)
        elif variation == 'fainter':
            if self.alpha > 0.8:
                return RGBA_Colour(variation + self.name, self.red, self.green, self.blue, self.alpha-0.8)

        return None
