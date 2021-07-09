#############################################################################
#
#
#   CSS Stylesheet webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a CSS module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the webclient of
bfa. Most importantly this class contains the CSS stylesheet class and makes elements of sub-modules available.

    Dependencies:

        css ------> rule
         |      |-> style
         v      \-> rules
        html -> node    @CSS_Stylesheet.toNode

        note::  Author(s): Mitch last-check: 07.07.2021 """

from typing import Union

from bfassist.webgen.framework.css.rule import CSS_Rule
from bfassist.webgen.framework.css.style import CSS_Style
from bfassist.webgen.framework.css.rules import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class CSS_Stylesheet:
    """ Representation of a CSS stylesheet.

        :param filename:    Filename of the stylesheet.
        :param styles:      Set of styles to be applied with this stylesheet.

            note::  Author(s): Mitch """

    def __init__(self, filename: str, styles: set = None):

        self.filename = filename

        if styles is not None and all([True if isinstance(Style, CSS_Style) else False for Style in styles]):
            self.styles = styles
        elif styles is None:
            self.styles = set()
        else:
            raise TypeError("All contents of styles must be CSS styles.")

    def __iadd__(self, other: Union[CSS_Style, set]):
        """ Function to add a CSS style to the sheet via the plus-equals-operator.

            :param other:   The CSS style to add.

            :return:        Returns itself at the end.

                note::  Author(s): Mitch """

        if isinstance(other, CSS_Style):
            self.styles.add(other)
        elif isinstance(other, set) and self.allStylesAreStyles(other):
            self.styles.update(other)
        return self

    @staticmethod
    def allStylesAreStyles(styles: set):
        """ Simple helper function to determine if all styles in a set of styles are actually css styles.

            :param styles:  The set of supposed styles.

            :return:        True if all styles are actual css styles, False otherwise.

                note::  Author(s): Mitch """

        return all([True if isinstance(Style, CSS_Style) else False for Style in styles])

    @staticmethod
    def toNode(path: str):
        """ Converts the stylesheet to a linkable node.

            :param path:    Relative path to the stylesheet.

                note::  Author(s): Mitch """

        from bfassist.webgen.framework.html.node import HTML_Node_Contentless

        return HTML_Node_Contentless('link', {'rel': 'stylesheet', 'href': path})

    def toString(self):
        """ Converts the stylesheet to a string.

            :return:    Stylesheet as string.

                note::  Author(s): Mitch """

        css = ""
        for Style in self.styles:
            css += Style.toString() + "\n"

        return css
