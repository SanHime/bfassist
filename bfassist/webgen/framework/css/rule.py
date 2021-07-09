#############################################################################
#
#
#   CSS Rule webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a CSS rule module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 07.07.2021 """


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class CSS_Rule:
    """ Representation of a single CSS rule.

        :param property:    Style property that's being defined.
        :param value:       Value to be defined.

            note::  Author(s): Mitch """

    def __init__(self, prop: str, val: str):
        self.property = prop
        self.value = val

    def toString(self):
        """ Converts a rule to a string.

            :return:    Rule as String.

                note::  Author(s): Mitch """

        return "\t" + self.property + ": " + self.value + ";\n"
