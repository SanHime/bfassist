#############################################################################
#
#
#   HTML form webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML form module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        bfassist <- (webgen.)framework <- html <- console
            |                   |        |
            |                   |        |-> node
            |                   |        \-> table
            |                   \         -> output
            \                    -> css
             -> api @Form.createInputFormForFunction, @Form.getScriptsForFillingFormsWithDataForFunctions,
                    @Form.getScriptForFillingFormWithDataForFunction

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from bfassist.webgen.framework.html.node import HTML_Node
from bfassist.webgen.framework.html.table import Table
from bfassist.webgen.framework.html.output import Output
from bfassist.webgen.framework.css import *
from bfassist.webgen.framework.js import JS_Function, JS_Function_Body


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Form(HTML_Node):
    """ A form object that should simplify the interactions with forms.

        :param Name:        Name of this form, should be unique among forms.
        :param script:      Tuple of JS functions used in this form.
        :param styles:      Set of CSS styles used in this form.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, script: tuple = None, styles: set = None):
        self.Name = Name
        if script:
            self.script = script
        else:
            self.script = ()
        if styles:
            self.styles = styles
        else:
            self.styles = set()
        super().__init__('form', Id=self.Name + 'InputForm', Class='inputForm')

    def styleForms(self):
        self.styles.add(self.styleThisClass({
            set_position('fixed'),
            set_width('100%')
        }))

    @classmethod
    def createInputFormForFunction(cls, func: BFA_FunctionApiMixIn, output: Output = None):
        """ Create an input form that can accept input for an api function using its type hints.

            :param func:    The api function to create an input form for.
            :param output:  The output element to direct the function output to, if specified.

                note::  Author(s): Mitch """

        from bfassist.standalone.api import BFA_FunctionApiMixIn

        form = cls(func.name)
        form += Fieldset(func.name)

        funcISO = func.generateSimpleISO()
        form.fieldset.Input += funcISO[0]
        form.fieldset.Submit += funcISO[1]
        if output:
            funcRequest = func.wrapISOwithJavaScript((funcISO[0], funcISO[1], output))
        else:
            funcRequest = func.wrapISOwithJavaScript((funcISO[0], funcISO[1], None))
        funcRequest.generateJSCode()
        form.script += (funcRequest,)
        return form

    def show(self):
        return "document.getElementById('" + self.Name + "InputForm').style.visibility = 'visible';"

    def hide(self):
        return "document.getElementById('" + self.Name + "InputForm').style.visibility = 'hidden';"

    @staticmethod
    def getScriptsForFillingFormsWithDataForFunctions(*functions: BFA_FunctionApiMixIn):
        from bfassist.standalone.api import BFA_FunctionApiMixIn
        JS = ()
        for func in functions:
            JS += (Form.getScriptForFillingFormWithDataForFunction(func), )
        return JS

    @staticmethod
    def getScriptForFillingFormWithDataForFunction(func: BFA_FunctionApiMixIn):
        from bfassist.standalone.api import BFA_FunctionApiMixIn

        return JS_Function(func.name + 'FillFormWithData', parameters=('data', ), body=JS_Function_Body(
            "let parameters = " + str(list(func.parameterTypeHints.keys())) + "\n"
            "for (const param of parameters) {\n"
            "\tif (param in data){\n"
            "\t\tdocument.getElementById('" + func.name + "' + param).value = data[param]\n"
            "\t}\n"
            "}\n"
        ))


class Fieldset(HTML_Node):
    """ A fieldset object that should simplify the interactions with fieldsets for forms.

        :param Name:    Name of this fieldset, should be unique among fieldsets.
        :param Layout:  A table layout with 2 columns for input and submitting input.
        :param Input:   The input side of the layout table.
        :param Submit:  The submit side of the layout table.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, Layout: Table = None, Input: HTML_Node = None, Submit: HTML_Node = None):
        self.Name = Name
        super().__init__('fieldset', Id=self.Name + 'Fieldset')
        if Layout:
            self.Layout = Layout
        else:
            self.Layout = Table.fromRowAndColumnCount(1, 2)
        self.__iadd__(self.Layout)
        if Input:
            self.Input = Input
        else:
            self.Input = self.Layout[0][0]
        if Submit:
            self.Submit = Submit
        else:
            self.Submit = self.Layout[0][1]
