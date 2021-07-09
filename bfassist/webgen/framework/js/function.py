#############################################################################
#
#
#   Javascript Function webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a javascript function module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining
the webclient of bfa.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class JS_Function_Body:
    """ Representation of a JS function body.

        :param code:    The JS code contained in the body.

            note::  Author(s): Mitch """

    def __init__(self, code: str = ""):
        self.code = code

    def __add__(self, other: JS_Function_Body):
        if isinstance(other, JS_Function_Body):
            self.code += other.code
            return self
        elif isinstance(other, str):
            self.code += other
            return self
        else:
            raise ValueError("Can only add another JS function body to a JS function body.")


class JS_Function:
    """ Representation of a single JS function.

        :param name:        Function name.
        :param parameters:  Function parameters.
        :param body:        Function body.

            note::  Author(s): Mitch """

    def __init__(self, name: str = "", parameters: tuple = None, body: JS_Function_Body = None):
        self.name = name
        if parameters:
            self.parameters = parameters
        else:
            self.parameters = ()

        if body is None:
            self.body = JS_Function_Body()
        else:
            self.body = body

    def toString(self):
        """ Converts the function to a string.

            :return:    Function as string.

                note::  Author(s): Mitch """

        js = "function " + self.name + "(" + ', '.join(self.parameters) + "){\n"

        js += "\t" + self.body.code.replace("\n", "\n\t") + "\n}\n"

        return js

    def call(self, parameters: tuple = None):
        """ Converts the function to a function call.

            :param parameters:  A tuple of parameters the function should be called with.

            :return:            Function call as string.

                note::  Author(s): Mitch """

        return self.name + "(" + ', '.join(parameters if parameters else self.parameters) + ")\n"

    def addCallsTo(self, *functions: JS_Function):
        """ Adds calls to other functions to the body.

            :param functions:   Functions to call.

                note::  Author(s): Mitch """

        for f in functions:
            if isinstance(f, JS_Function):
                self.body += f.name + "()\n"
