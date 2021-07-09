#############################################################################
#
#
#   Module Mix In API Module
#
#
#############################################################################
""" An intermediary module required for our actual ends registering functions and turning them into API functions.

    Dependencies:

        apimodule
            |
            v
        apifunction @ModuleApiMixIn.mixInFunction()

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ModuleApiMixIn:
    """ Objects of this class represent a python module that have at least one function inside that should be callable
    from the api. So the api functionality gets mixed in by improving our introspective ability.

        :param name:                    The name of this module.
        :param relative_path:           The relative path to this module that's used to identify/find this module.
                                        (Does not actually end with the correct file name but with the module name)
        :param mixed_in_functions:      A dictionary of api-mixed-in functions contained in this module. The function
                                        name is the key to the function itself as value.
        :param mixed_in_sub_modules:    A dictionary of further api-mixed-in sub modules of this module.

            note::  Author(s): Mitch """

    def __init__(self, name: str, relative_path: str, mixed_in_functions: dict = None,
                 mixed_in_sub_modules: dict = None):
        self.name = name
        self.relative_path = relative_path

        if mixed_in_functions:
            self.mixed_in_functions = mixed_in_functions
        else:
            self.mixed_in_functions = {}
        if mixed_in_sub_modules:
            self.mixed_in_sub_modules = mixed_in_sub_modules
        else:
            self.mixed_in_sub_modules = {}

    def propagateRegistration(self, sub_modules: list):
        """ Function that propagates the registration of a list of sub modules of this module in case any of them have
        not yet been instantiated. And returns the last instantiated module.

            :param sub_modules: The list of sub modules.

            :return:            The api-mix-in sub module that was last instantiated.

                note::  Author(s): Mitch """

        if sub_modules[0] not in self.mixed_in_sub_modules:
            self.mixed_in_sub_modules[sub_modules[0]] = ModuleApiMixIn(sub_modules[0],
                                                                       self.relative_path + "/" + sub_modules[0])
        if len(sub_modules) > 1:
            return self.mixed_in_sub_modules[sub_modules[0]].propagateRegistration(sub_modules[1:])
        else:
            return self.mixed_in_sub_modules[sub_modules[0]]

    def mixInFunction(self, func: FunctionApiMixIn):
        """ Function that mixes in api-availability to the passed function.

            :param func:    The function that should be available from the api.

                note::  Author(s): Mitch """

        from bfassist.api import FunctionApiMixIn

        self.mixed_in_functions[func.name] = func

    def __contains__(self, item):
        return item in self.mixed_in_sub_modules or item in self.mixed_in_functions

    def __getitem__(self, item):
        if item in self.mixed_in_sub_modules:
            return self.mixed_in_sub_modules[item]
        elif item in self.mixed_in_functions:
            return self.mixed_in_functions[item]
        else:
            raise ValueError("Item " + item + " not in " + self.name + ".")
