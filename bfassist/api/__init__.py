#############################################################################
#
#
#   API modules for BF-A mainly for the api of the webservice of the bfa standalone
#
#
#############################################################################
""" This module can set up a simple API. The design of the API follows simplified principles of a REST-API. Three base
HTTP request types are supposed to be supported though the hooking of the API to a webserver is not provided for in this
module. However, the bfa webservice can be used for that. If so desired the API could also be made available from a
different interface.

The three request types GET, PUT and POST are used to structure the API.

GET requests are supposed to return an element and not cause any modifications.

PUT requests should return no elements but only boolean values to indicate the request could or could not be completed.

POST requests are most commonly used to submit or create new elements and usually return the created element.


In order to make a python function available from the API you need to register, "mix" it into the API. This is done by
calling the respective request type function on the function you want to register. Best practise would be to call it
immediately after the definition of the function.

Example:

from bfa_api import api_POST

def foo(bar: object) -> object:
    return bar
api_POST(foo)


For the API to work properly the registered functions should be fully type-hinted. Due to the lack of TypedDicts in
Python3.7 and the inconvenience in upgrading the python version for the bfa project as a whole, a bit of trickery is
required for type-hinting some more complex return types. For instance object-attribute formats can not be properly
type-hinted without the presence of TypedDicts. For that reason dictionaries in type-hints are always assumed to follow
an object-attribute structure. In case a dictionary is an actual dictionary or even a set then a key '__type__' will
contain the actual type this dictionary is hinting at, '__values__' will hint at the type of values stored and if it's
an actual dictionary '__keys__' will hint at the type of the keys.

Example set:
{
    '__type__': set,
    '__values__': RealTimePlayer.typeHint(),
}

Example dict:
{
    '__type__': dict,
    '__keys__': str,
    '__values__': RealTimePlayer.typeHint()
}

Example object-attribute format:

{
    'Keyhash': str,
    'Rights': BFARight.typeHint(),
    'User': str,
    'Pass': str,
    'Online': int,
    'MultiLogin': bool
}

The default request url for an api function can be built, as is done for the standalone, in the following way:
(compare standalone.webservice BFA_API_RequestHandler)

https://<name>:444/<root-module.submod.subsubmod... turns into module/submod/subsubmod/...>/functionName

GET-requests:
If there is a key required for finding the element the parameters would have to be sent with the URL if required.
The standalone web service uses the format '../function/params?param1=value1&param2=value2...'.

POST-requests:
Request parameters are also to be sent in the request body in json-format and usually return the created element or the
element affected by them.

PUT-requests:
Request parameters are to be sent in the request body in json-format.

This is consistent with the need for a well-defined module and function namespace in python. However, it also means
that only the module scope is properly reachable. If you want to make nested name-spaces available they have to be
somehow callable from the module scope. In the bfa standalone for instance all API functions are static and get invoked
from the bfa KERN. The KERN even has a dedicated API module but in principle it would also be possible to register
the functions directly from their respective module rather than a dedicated API module.

The webservice can then be used to find the function from the API_MODULES dictionary by calling:

from bfa_api import API_MODULES

func = API_MODULES[module][submodule][...].mixed_in_functions['function_name']

Using the type hints at func.parameterTypeHints the function can then easily be called properly and the response can be
customised and composed using the func.returnTypeHint. Example usages can be found in the standalone api.

    Dependencies:

    api ---\-> apimodule
            -> apifunction

        note::  Author(s): Mitch last-check: 07.07.2021 """

from inspect import getmodule
from copy import deepcopy

from bfassist.api.apimodule import ModuleApiMixIn
from bfassist.api.apifunction import FunctionApiMixIn


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


API_MODULES = {}


def getFunctions(apiModules: dict):
    """ A function to extract a list of all functions that can be found in an api modules dictionary.
    ::important::   This function mutates the input parameter so it should be called with a copy of the original.

        :param apiModules:  A dictionary containing all api modules and functions according to their structure.

        :return:            A list of all functions contained in the dictionary.

            note::  Author(s): Mitch """

    functions = []
    while apiModules:
        key, value = apiModules.popitem()
        if isinstance(value, FunctionApiMixIn):
            functions.append(value)
        else:
            if value:
                functions.extend(list(value.mixed_in_functions.values()))
                functions.extend(getFunctions(value.mixed_in_sub_modules))
    return functions


def api_mix_in_modules(module_list: list):
    """ Function to register/mix-in the api to a hierarchical list of modules and finally returns the lowest specified
    module. If all modules were previously registered/mixed-in to the api then it'll just return the lowest module.

        :param module_list: The list of modules to register where each successive list entry is a sub module of the
                            previous list entry.

        :return:            The last module of the list as api-mix-in module.

            note::  Author(s): Mitch """

    if module_list[0] not in API_MODULES:
        API_MODULES[module_list[0]] = ModuleApiMixIn(module_list[0], module_list[0])

    last_module = API_MODULES[module_list[0]]
    if len(module_list) > 1:
        last_module = API_MODULES[module_list[0]].propagateRegistration(module_list[1:])

    return last_module


def api_GET(func: callable):
    """ An init that will hook a function to the API and make it available via GET requests.

        :param func:    The function to mix into the API.

            note::  Author(s): Mitch """

    last_module = api_mix_in_modules(getmodule(func).__name__.split('.'))
    apiF = FunctionApiMixIn.new(func, 'GET', last_module)
    if apiF is None:
        last_module.mixInFunction(FunctionApiMixIn(func, 'GET', last_module))
    else:
        last_module.mixInFunction(apiF)


def api_PUT(func: callable):
    """ An init that will hook a function to the API and make it available via PUT requests.

        :param func:    The function to mix into the API.

            note::  Author(s): Mitch """

    last_module = api_mix_in_modules(getmodule(func).__name__.split('.'))
    apiF = FunctionApiMixIn.new(func, 'PUT', last_module)
    if apiF is None:
        last_module.mixInFunction(FunctionApiMixIn(func, 'PUT', last_module))
    else:
        last_module.mixInFunction(apiF)


def api_POST(func: callable):
    """ An init that will hook a function to the API and make it available via POST requests.

        :param func:    The function to mix into the API.

            note::  Author(s): Mitch """

    last_module = api_mix_in_modules(getmodule(func).__name__.split('.'))
    apiF = FunctionApiMixIn.new(func, 'POST', last_module)
    if apiF is None:
        last_module.mixInFunction(FunctionApiMixIn(func, 'POST', last_module))
    else:
        last_module.mixInFunction(apiF)
