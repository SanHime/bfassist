#############################################################################
#
#
#   Function Mix In API Module
#
#
#############################################################################
""" Module that defines the FunctionApiMixIn class that acts as request interface for a single python function.

The class can be inherited to implement additional features. An example for that can be found in the standalone api
module that introduces URL-building and standardised HTML, JS generation.

The new method replaces the init because overriding the init would not properly work as I intended. Probably because I'm
using a lot of un-pythonic import trickery. Perhaps ABCs could solve this in a better way but I'm unfamiliar with them
and this does work :).

    Dependencies:

        apifunction
            |
            v
        apimodule

        note::  Author(s): Mitch last-check: 07.07.2021 """

from typing import get_type_hints

from bfassist.api.apimodule import ModuleApiMixIn


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class FunctionApiMixIn:
    """ Objects of this class represent functions in api-mixed-in modules. The return of a mixed in function needs to be
    json-serializable.

        :param func:                The actual python function that's supposed to get mixed in.
        :param apiRequestType:      With which request type this function can be reached.
        :param module:              The api-mix-in module this function belongs to.
        :param parameterTypeHints:  The type hints for the input-parameters.
        :param returnTypeHint:      The return type-hint.

        :param name:            The name of the function.

            note::  Author(s): Mitch """

    def __init__(self, func: callable, apiRequestType: str, module: ModuleApiMixIn, parameterTypeHints: dict = None,
                 returnTypeHint: dict = None, name: str = None):

        func.apiMixIn = self
        self.func = func
        self.apiRequestType = apiRequestType
        self.module = module

        if parameterTypeHints and returnTypeHint:
            self.parameterTypeHints = parameterTypeHints
            self.returnTypeHint = returnTypeHint
        else:
            typeHints = get_type_hints(self.func)
            self.returnTypeHint = typeHints.pop('return')
            self.parameterTypeHints = typeHints

        if name:
            self.name = name
        else:
            self.name = func.__name__

    @classmethod
    def new(cls, func: callable, apiRequestType: str, module: ModuleApiMixIn):
        """ To be overridden. """
        return None
