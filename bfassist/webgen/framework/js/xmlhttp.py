#############################################################################
#
#
#   Javascript xmlHttp Function webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a javascript xmlHttp function module for a simple HTML/JS/CSS generator/framework with the purpose of
maintaining the webclient of bfa.

    Dependencies:

        bfassist <- webgen <- framework <- (js.)xmlhttp
            |                   |
            |                   \-> html
            \                    -> js -> function
             -> webgen  @Request.redirectOnSuccess

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from bfassist.webgen.framework.html import SimpleOutput, ButtonInput
from bfassist.webgen.framework.html.userinput import Input
from bfassist.webgen.framework.js.function import JS_Function, JS_Function_Body


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class RequestPostProcessing(JS_Function):
    """ Standard for XMLHttpRequest post processing function.

        :param successProcession:   JS function body that defines what to do if the request succeeded.
        :param successProcession:   JS function body that defines what to do if the request failed.

            note::  Author(s): Mitch """

    def __init__(self, successProcession: JS_Function_Body = None, failureProcession: JS_Function_Body = None):
        super().__init__()
        self.successProcession = successProcession
        self.failureProcession = failureProcession

    def postProcessOnSuccess(self, successProcession: JS_Function_Body):
        self.successProcession = successProcession
        if self.successProcession:
            code = self.successProcession.code.replace('\n', '\n\t')
        else:
            code = ""
        self.body.code = "if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {\n" \
                         "\t" + code + "}\n"

    def postProcessOnFailure(self, failureProcession: JS_Function_Body):
        self.failureProcession = failureProcession
        if self.failureProcession:
            code = self.failureProcession.code.replace('\n', '\n\t')
        else:
            code = ""
        self.body.code += "if (xmlhttp.readyState === 4 && xmlhttp.status !== 200) {\n" \
                          "\t" + code + "}\n"

    def generateJSCode(self):
        self.postProcessOnSuccess(self.successProcession)
        self.postProcessOnFailure(self.failureProcession)

    def useSimpleOutput(self, output: SimpleOutput, responseType: str):
        if responseType == 'json':
            self.successProcession += output.assign("JSON.stringify(xmlhttp.response)\n")
            self.failureProcession += output.assign("JSON.stringify(xmlhttp.response)\n")
        else:
            self.successProcession += output.assign("xmlhttp.response\n")
            self.failureProcession += output.assign("xmlhttp.response\n")


class RequestParameter:
    """ Simple helper class to make adding request parameters more readable in python.

        :param Name:    The name of the parameter.
        :param Node:    The node this parameter can be read from.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, Node: Input):
        self.Name = Name
        self.Node = Node

    def __add__(self, other):
        if isinstance(other, str):
            return "\'" + self.Name + "\'" + other
        elif isinstance(other, JS_Function_Body):
            return "\'" + self.Name + "\'" + other.code
        else:
            raise ValueError("Can only add request parameter to str or js function body.")

    def __radd__(self, other):
        if isinstance(other, str):
            return other + "\'" + self.Name + "\'"
        elif isinstance(other, JS_Function_Body):
            return other.code + "\'" + self.Name + "\'"
        else:
            raise ValueError("Can only add request parameter to str or js function body.")


class Request(JS_Function):
    """ Standard for performing an XML Http Request.

        :param url:                     The url to send to.
        :param requestType:             The request type.
        :param requestBodyParameters:   A set of request parameters that will be fitted inside the request body unless
                                        it's a GET request in which case they will be filled to the url.
        :param calledFrom:              The input node that can call this request.
        :param outputTo:                The output nodes as tuple that the result of the request will be written to.
        :param responseType:            The response type.

        :param post_processing:         The post processing function.

            note::  Author(s): Mitch """

    def __init__(self, name: str, url: str, requestType: str, requestBodyParameters: set = None,
                 calledFrom: ButtonInput = None, outputTo: tuple = None, responseType: str = 'json',
                 post_processing: RequestPostProcessing = None):
        super().__init__(name)
        self.url = url
        self.requestType = requestType
        if requestBodyParameters:
            self.requestBodyParameters = requestBodyParameters
        else:
            self.requestBodyParameters = {}
        self.calledFrom = calledFrom
        self.outputTo = outputTo
        self.responseType = responseType
        self.post_processing = post_processing

    def createNewXMLHttpRequest(self):
        self.body.code = "let xmlhttp = new XMLHttpRequest()\n"

    def defineRequestURL(self):
        self.body.code += "let url = '" + self.url + "'\n"

    def defineRequestBodyParameters(self, requestBodyParameters: dict):
        if requestBodyParameters:
            self.requestBodyParameters = requestBodyParameters
            self.body.code += "let parameters = {\n"
            for parameter in self.requestBodyParameters:
                self.body.code += "\t " + parameter + " : " + parameter.Node.read() + ",\n"
            self.body.code = self.body.code[:-2] + "\n" \
                                                   "}\n"
            if self.requestType == 'GET':
                self.addGETparametersToRequest()

    def setResponseType(self, responseType: str = 'json'):
        self.responseType = responseType
        self.body.code += "xmlhttp.responseType = \"" + self.responseType + "\"\n"

    def openRequest(self):
        self.body.code += "xmlhttp.open('" + self.requestType + "', url, true)\n"

    def onReadyStateChange(self, post_processing: RequestPostProcessing):
        self.post_processing = post_processing
        self.body.code += "xmlhttp.onreadystatechange = " + \
                          (post_processing.toString() if isinstance(post_processing, RequestPostProcessing) else
                           "function(){}\n")

    def sendRequest(self):
        self.body.code += "if (typeof parameters !== 'undefined') " \
                     "{xmlhttp.send(JSON.stringify(parameters))} else " \
                     "{xmlhttp.send()}"

    def generateJSCode(self):
        self.createNewXMLHttpRequest()
        self.defineRequestURL()
        self.defineRequestBodyParameters(self.requestBodyParameters)
        self.setResponseType(self.responseType)
        self.openRequest()
        if self.post_processing is None and self.outputTo is not None:
            self.generateSimpleOutputPostProcessing()
        self.onReadyStateChange(self.post_processing)
        self.sendRequest()

        if self.calledFrom is not None and self.calledFrom.onClick != self:
            self.hookFunctionToCaller()

    def addGETparametersToRequest(self):
        self.body.code += "url += '/params?'\n" \
                     "for (const [key, value] of Object.entries(parameters)) {\n" \
                     "\t    url += key + '=' + value + '&'\n" \
                     "}\n" \
                     "url = url.slice(0, -1)\n"

    def generateSimpleOutputPostProcessing(self):
        if isinstance(self.outputTo, tuple):
            if len(self.outputTo) == 1 and isinstance(self.outputTo[0], SimpleOutput):
                outputTo = self.outputTo[0]
            else:
                raise ValueError("Can only generate simple output for a single node of simple output but received " +
                                 str(self.outputTo))
        else:
            outputTo = self.outputTo

        self.post_processing = RequestPostProcessing(JS_Function_Body(), JS_Function_Body())
        self.post_processing.useSimpleOutput(outputTo, self.responseType)
        self.post_processing.generateJSCode()

    def hookFunctionToCaller(self):
        self.calledFrom.setOnClick(self)

    def redirectOnSuccess(self, redirection: View):
        from bfassist.webgen import View

        self.post_processing.successProcession += 'window.location.href = "' + redirection.Name + '"\n'
        self.post_processing.generateJSCode()
        self.generateJSCode()

    def callOnSuccess(self, func: JS_Function):
        if self.post_processing is None:
            self.post_processing = RequestPostProcessing(JS_Function_Body(func.name + '()\n'))
        else:
            self.post_processing.successProcession += func.name + '()\n'
        self.post_processing.generateJSCode()
        self.generateJSCode()
