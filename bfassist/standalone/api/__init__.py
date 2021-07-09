#############################################################################
#
#
#   BFA standalone API
#
#
#############################################################################
""" API for the bfa standalone adding some functionality especially for the webclient in regard of generating views.

    Dependencies:

        bfassist <- (standalone.)api
            |
            |-> api
            |-> framework --\-> html
            \                -> js -> xmlhttp
             -> standalone -> api ----> get
                                    \-> post
                                     -> put

        note::  Author(s): Mitch last-check: 08.07.2021 """

from __future__ import annotations

from bfassist.api import FunctionApiMixIn, API_MODULES
from bfassist.webgen.framework.html import *
from bfassist.webgen.framework.js.xmlhttp import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BFA_FunctionApiMixIn(FunctionApiMixIn):
    """ Extending the API to support useful features for interacting with JS XMLHTTPRequests.

            note::  Author(s): Mitch """

    def buildStandardUrl(self):
        """ Function that builds the standard url this function can be reached from.

            :return:    The standard url this function should be reached at.

                note::  Author(s): Mitch """

        return "/".join([self.module.relative_path, self.name])

    def generateSimpleISO(self):
        """ Function that generates the required HTML input, submit and output elements for JS to call this function
         from a web-browser.

            :return:    The HTML input, submit and output elements as tuple. The input and output elements are tuples.

                note::  Author(s): Mitch """

        layoutTableBody = TableBody()

        for param in self.parameterTypeHints:
            if param == 'Pass':
                layoutTableBody += TableRow((td((LabeledInput(param, self.name + param, 'password'), )), ))
            else:
                layoutTableBody += TableRow((td((LabeledInput(param, self.name + param), )), ))

        functionInput = Table(tableBodies=(layoutTableBody, ))

        functionSubmit = ButtonInput()
        functionOutput = SimpleOutput()
        functionOutput.Id = self.name + 'Output'

        return functionInput, functionSubmit, functionOutput

    def wrapISOwithJavaScript(self, ISO: tuple = None, non_standard_url: str = None, submitButtonValue: str = None):
        """ Function that links the required HTML input, submit and output elements via JS with this function.

            :param ISO:                         A tuple containing tuples of input, submit and output elements required
                                                for wrapping.

            :param non_standard_url:            If this function is available from a non-standard url then this url
                                                should be specified here.
            :param submitButtonValue:           The value of the submit button in case it should not just say "Submit".

            :return:                            The JS request function that contains all required JS to wrap the
                                                elements.

                note::  Author(s): Mitch """

        if ISO is None:
            ISO = self.generateSimpleISO()
        InputTable, Submit, OutputNode = ISO

        if non_standard_url:
            url = non_standard_url
        else:
            url = self.buildStandardUrl()

        requestParameters = set()
        if InputTable:
            if isinstance(InputTable, ScrollTable):
                InputTable = InputTable.table
            for parameterInputRow in InputTable.tbody:
                requestParameters.add(RequestParameter(parameterInputRow.td.label.label, parameterInputRow.td.label))

        responseType = 'json'
        if self.returnTypeHint == bool:
            responseType = 'text'

        if submitButtonValue:
            Submit.innerHTML = submitButtonValue

        return Request(self.name + 'Request', url, self.apiRequestType, requestParameters, Submit, OutputNode,
                       responseType)

    def fillScrollTableWithFunctionOutput(self, scrollTable):
        """ Function that links the output of this function to a scroll table and returns JS to fill it.

            :return:    The JS request function that contains all required JS.

                note::  Author(s): Mitch """

        post_processing = scrollTable.getPostProcessingForRequestDataForThisScrollTable()
        post_processing.generateJSCode()
        return Request(self.name + 'Request', self.buildStandardUrl(), self.apiRequestType, None, None, None,
                       'json', post_processing)


def new(func: callable, requestType: str, module: ModuleApiMixIn):
    return BFA_FunctionApiMixIn(func, requestType, module)


FunctionApiMixIn.new = new


class bfaAPI:
    """ The api class for bfa standalone.

        :param KERN:        The bfa kern the api is connected with.
        :param by_modules:  The actual api module dictionary.

        :param get_api:     The get requests served by the api.
        :param put_api:     The put requests served by the api.
        :param post_api:    The post requests served by the api.

            note::  Author(s): Mitch """

    def __init__(self, KERN: BFAKern, by_modules: dict = API_MODULES, get_api: api_GETs = None,
                 put_api: api_PUTs = None, post_api: api_POSTs = None):

        from bfassist.standalone import BFAKern
        from bfassist.standalone.api.get import api_GETs
        from bfassist.standalone.api.post import api_POSTs
        from bfassist.standalone.api.put import api_PUTs

        self.KERN = KERN
        self.by_modules = by_modules

        if get_api:
            self.GET_API = get_api
        else:
            self.GET_API = api_GETs(self.KERN)

        if post_api:
            self.POST_API = post_api
        else:
            self.POST_API = api_POSTs(self.KERN)

        if put_api:
            self.PUT_API = put_api
        else:
            self.PUT_API = api_PUTs(self.KERN)
