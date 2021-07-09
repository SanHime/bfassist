#############################################################################
#
#
#   CSS Style webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a CSS style module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        css <- style

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webgen.framework.css import CSS_Rule


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class CSS_Style:
    """ Representation of CSS styling for a single instance.

        :param target:  The target specification for the style to be applied to.
        :param rules:   Set of style rules to be applied.

            note::  Author(s): Mitch """

    def __init__(self, target: str, rules: set):
        self.target = target

        if all([True if isinstance(rule, CSS_Rule) else False for rule in rules]):
            self.rules = rules
        else:
            raise TypeError("All contents of rules must be CSS rules.")

    def toString(self):
        """ Converts a style to a string.

            :return:    Style as string.

                note::  Author(s): Mitch """

        css = self.target + " {\n"

        for rule in self.rules:
            css += rule.toString()

        css += "}\n"

        return css
