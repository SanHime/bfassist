#############################################################################
#
#
#   Javascript Script webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a javascript script module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa. Most importantly this module contains the JS script class and makes elements of sub-modules available.

    Dependencies:

        framework <- js
            |
            \-> html
             -> js -> function

        note::  Author(s): Mitch last-check: 07.07.2021 """

from typing import Union

from bfassist.webgen.framework.html import HTML_Node
from bfassist.webgen.framework.js.function import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class JS_Script:
    """ Representation of a Javascript script.

        :param filename:    Filename of the JS script.
        :param functions:   Dictionary of JS functions with the function names as keys.

            note::  Author(s): Mitch """

    def __init__(self, filename: str, functions: dict = None):
        self.filename = filename

        if functions is not None and all([True if isinstance(Function, JS_Function)
                                          else False for Function in functions]):
            self.functions = functions
        elif functions is None:
            self.functions = {}
        else:
            raise TypeError("All contents of functions must be JS functions.")

    def __iadd__(self, other: Union[JS_Function, tuple]):
        """ Function to add a JS function to the script via the plus-equals-operator.

            :param other:   The JS function to add.

            :return:        Returns itself at the end.

                note::  Author(s): Mitch """
        if isinstance(other, JS_Function):
            self.functions[other.name] = other
        elif isinstance(other, tuple) and self.allFunctionsAreFunctions(other):
            for Function in other:
                self.functions[Function.name] = Function
        return self

    @staticmethod
    def allFunctionsAreFunctions(functions: tuple):
        """ Simple helper function to determine if all functions in a tuple are actually JS functions.

            :param functions:   A tuple of supposed functions.

            :return:            True if all functions are actually JS functions.

                note::  Author(s): Mitch """

        return all(True if isinstance(Function, JS_Function) else False for Function in functions)

    @staticmethod
    def toNode(path: str):
        """ Converts the script to a linkable node.

            :param path:    Relative path to the script.

                note::  Author(s): Mitch """

        return HTML_Node('script', {'type': 'text/javascript', 'src': path})

    def toString(self):
        """ Converts the script to a string.

            :return:    Script as string.

                note::  Author(s): Mitch """

        js = ""

        for functionName in self.functions:
            Function = self.functions[functionName]
            if isinstance(Function, JS_Function):
                js += Function.toString() + "\n"
            else:
                js += "\n"

        return js
