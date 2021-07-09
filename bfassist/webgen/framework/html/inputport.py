#############################################################################
#
#
#   HTML input port webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML input port module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        bfassist <- (webgen.)framework <- html <- inputport
            |                   |           \-> userinput
            |                   \            -> form
            \                    -> css
             -> api @InputPort.show, @InputPort.hide

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from bfassist.webgen.framework.html import HTML_Node, ScrollTable
from bfassist.webgen.framework.html.userinput import PseudoButtonInput, Select
from bfassist.webgen.framework.html.form import Form
from bfassist.webgen.framework.css.rules import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class InputPort(HTML_Node):
    """ An input port object that should simplify the interactions with input ports. This object is a div container
    with input options for the user to enter info for an API request.

        :param Name:            Name of this input port.
        :param inputFunctions:  A tuple of functions this input port should supply input for.
        :param script:          A tuple of JS for this input port.
        :param styles:          A set of CSS styles for this input port.
        :param inputForms:      A dictionary of functions this input port should supply input for and their forms.
        :param closeButton:     Close button of this input port.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, inputFunctions: tuple, script: tuple = None, styles: set = None,
                 inputForms: dict = None, closeButton: HTML_Node = None):
        self.Name = Name
        if inputFunctions:
            self.inputFunctions = inputFunctions
        else:
            self.inputFunctions = ()

        if script:
            self.script = script
        else:
            self.script = ()
        if styles:
            self.styles = styles
        else:
            self.styles = set()

        if inputForms:
            self.inputForms = inputForms
        else:
            self.inputForms = {inputFunction: None for inputFunction in self.inputFunctions}
        super().__init__('div', Id=self.Name + 'InputPortWrapper', Class='inputPortWrapper')

        if closeButton:
            self.closeButton = closeButton
        else:
            self.closeButton = self.addCloseButton()
        self.addFormSelector()

        for inputFunction in self.inputForms:
            self.inputForms[inputFunction] = self.addFormToSelect(Form.createInputFormForFunction(inputFunction))

        self.select.generateDefaultOnChange()
        self.closeButton.setOnClick(self.hide(*self.inputFunctions))

        self.form.styleForms()
        self.styles.update(self.form.styles)

    def hide(self, *functions: FunctionApiMixIn):
        from bfassist.api import FunctionApiMixIn

        code = "document.getElementById('" + self.Name + "InputPortWrapper').style.visibility = 'hidden';"
        if functions:
            code += self.hideOptionsOfFunctions(functions)
        return code

    def hideOptionsOfFunctions(self, functions: tuple):
        code = ""
        for func in functions:
            code += self.select.hideOptionAndForm(self.inputForms[func])
        return code

    def show(self, *functions: FunctionApiMixIn):
        from bfassist.api import FunctionApiMixIn
        code = "document.getElementById('" + self.Name + "InputPortWrapper').style.visibility = 'visible';"
        if functions:
            code += self.showOptionsOfFunctions(functions)
        return code

    def showOptionsOfFunctions(self, functions: tuple):
        code = ""
        defaultSet = False
        for func in functions:
            if defaultSet:
                code += self.select.showOption(self.inputForms[func])
            else:
                code += self.select.showOptionAndForm(self.inputForms[func])
                defaultSet = True
        return code

    def addCloseButton(self):
        closeButton = PseudoButtonInput(nodeType='div')
        closeButton.Id = self.Name + 'InputPortCloseButton'
        closeButton.innerHTML = '&#10006;'
        self.appendChildNode(closeButton)
        self.styles.add(closeButton.styleThisNode({
            set_cursor('pointer'),
            set_text_align('right'),
            set_margin_right('30px')
        }))
        return closeButton

    def addFormSelector(self):
        select = Select()
        select.Id = self.Name + 'InputPortSelector'
        select.Class = 'inputPortSelector'
        self.appendChildNode(select)

    def addFormToSelect(self, inForm: Form):
        """ Function to add a html input form to the selector that can be switched to using JS.

            :param inForm:  The form to be added as option.

            :return:        Returns the form at the end.

                note::  Author(s): Mitch """

        self.select.addOption(inForm)
        self.styles.add(self.select.options[inForm].styleThisNode({
            set_visibility('hidden')
        }))
        self.styles.add(inForm.styleThisNode({
            set_visibility('hidden')
        }))
        self.appendChildNode(inForm)
        self.script += inForm.script

        return inForm

    def styleInputPort(self, backGroundColour: Colour, borderColour: RGB_Colour):
        """ Function that adds the required CSS styles to the input ports.

                note::  Author(s): Mitch """

        self.styles.add(self.styleThisClass({
            set_position('absolute'),
            set_top('50%'),
            set_left('50%'),
            set_transform('-50%', '-50%'),
            set_width('600px'),
            set_height('300px'),
            set_font_weight('bold'),
            set_background_colour(backGroundColour),
            set_text_align('center'),
            set_border('2px', 'solid', borderColour),
            set_border_radius('15px'),
            set_visibility('hidden')
        }))
