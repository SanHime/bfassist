#############################################################################
#
#
#   webGen framework HTML user-input module to BFA v.5 standalone
#
#
#############################################################################
""" Module to improve python to HTML coding with the bfa webGen modules.

    Dependencies:

        framework <- html <- userinput
            |           \
            \            -> form
             -> js

        note::  Author(s): Mitch last-check: 07.07.2021 """

from typing import Union

from bfassist.webgen.framework.html import HTML_Node, option
from bfassist.webgen.framework.html.form import Form
from bfassist.webgen.framework.js import JS_Function


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Input(HTML_Node):
    """ An input object that should simplify the interactions with inputs.

        :param inputType:   The input type.
        :param properties:  Any properties this input has excluding it's input type.

            note::  Author(s): Mitch """

    def __init__(self, inputType: str, properties: dict = None):
        if properties:
            properties['type'] = inputType
        else:
            properties = {'type': inputType}
        super().__init__('input', properties)


class TextInput(Input):
    """ A text input object that should simplify the interactions with text-inputs.

        :param inputType:   The text input type which is text by default.
        :param maxlength:   The maximum number of characters allowed for this text input.
        :param size:        Specifies the reserved width for this text input measured in characters.

            note::  Author(s): Mitch """

    def __init__(self, inputType: str = 'text', maxlength: int = 32, size: int = 32):
        super().__init__(inputType, {'maxlength': str(maxlength), 'size': str(size)})


class PasswordInput(TextInput):
    """ A password input object that should simplify the interactions with password-inputs.

        :param maxlength:   The maximum number of characters allowed.
        :param size:        Specifies the reserved width for this input measured in characters.

            note::  Author(s): Mitch """

    def __init__(self, maxlength: int = 32, size: int = 32):
        super().__init__('password', maxlength, size)


class LabeledInput(HTML_Node):
    """ A labeled input object that should simplify the interactions with labeled inputs.

        :param label:       The actual innerHTML of the label element.
        :param bindingId:   The id value of the labeled input element used to bind them together.
        :param inputType:   The input type.

        :param inputNode:   The actual input object.

            note::  Author(s): Mitch """

    def __init__(self, label: str, bindingId: str, inputType: str = 'text', inputNode: Input = None):
        super().__init__('label', {'for': bindingId})
        self.innerHTML = label
        self.label = label
        if inputNode:
            self.inputNode = inputNode
        elif inputType == 'password':
            self.inputNode = PasswordInput()
        else:
            self.inputNode = TextInput()
        self.inputNode.Id = bindingId
        self.appendChildNode(self.inputNode)

    def read(self):
        return "document.getElementById('" + self.inputNode.Id + "').value"


class ButtonInput(HTML_Node):
    """ A button object that should simplify the interactions with buttons.

        :param onClick:     The JS function to call on click.
        :param innerHTML:   The value written on the button.

            note::  Author(s): Mitch """

    def __init__(self, innerHTML: str = "Submit", onClick: Union[JS_Function, str] = ""):
        self.onClick = onClick
        super().__init__('button', {'onClick': self.onClick.name + "()"
                         if isinstance(self.onClick, JS_Function) else onClick, 'type': 'button'}, innerHTML)

    def setOnClick(self, onClick: Union[JS_Function, str]):
        if isinstance(onClick, JS_Function):
            self.onClick = onClick
            self.properties['onClick'] = onClick.name + '()'
        else:
            self.onClick = onClick
            self.properties['onClick'] = onClick


class PseudoButtonInput(HTML_Node):
    """ An object used as pseudo button input object that should simplify the interactions with such inputs.

        :param onClick:     The JS function to call on click.
        :param nodeType:    The node type of the pseudo button.

            note::  Author(s): Mitch """

    def __init__(self, onClick: Union[JS_Function, str] = "", nodeType: str = 'a'):
        self.onClick = onClick
        super().__init__(nodeType, {'onClick': self.onClick.name + "()" if isinstance(self.onClick, JS_Function) else
                                    onClick})

    def setOnClick(self, onClick: Union[JS_Function, str]):
        if isinstance(onClick, JS_Function):
            self.onClick = onClick
            self.properties['onClick'] = onClick.name + '()'
        else:
            self.onClick = onClick
            self.properties['onClick'] = onClick


class Select(HTML_Node):
    """ A select object that should simplify the interactions with selects.

        :param onChange:    JS select function to call.
        :param value:       The value chosen by default.
        :param options:     The values one can choose from with this select as dictionary.

            note::  Author(s): Mitch """

    def __init__(self, onChange: Union[JS_Function, str] = "", value: str = "", options: dict = None):
        self.onChange = onChange
        self.value = value
        super().__init__('select', {'onChange': self.onChange.name + '(this)' if isinstance(self.onChange, JS_Function)
                                    else onChange, 'value': self.value})
        if options:
            self.options = options
        else:
            self.options = {}

    def setOnChange(self, onChange: Union[JS_Function, str]):
        if isinstance(onChange, JS_Function):
            self.onChange = onChange
            self.properties['onChange'] = onChange.name + '(this)'
        else:
            self.onChange = onChange
            self.properties['onChange'] = onChange

    def addOption(self, inForm: Form):
        opt = option(inForm.Name)
        opt.properties['value'] = inForm.Name
        opt.Id = inForm.Name + "Option"
        self.appendChildNode(opt)
        self.options[inForm] = opt

    def showOptionAndForm(self, inForm: Form):
        return "document.getElementById('" + inForm.Name + "Option').style.visibility = 'visible';" + inForm.show() + \
               self.setValue(inForm)

    @staticmethod
    def showOption(inForm: Form):
        return "document.getElementById('" + inForm.Name + "Option').style.visibility = 'visible';"

    @staticmethod
    def hideOptionAndForm(inForm: Form):
        return "document.getElementById('" + inForm.Name + "Option').style.visibility = 'hidden';" + inForm.hide()

    @staticmethod
    def hideOption(inForm: Form):
        return "document.getElementById('" + inForm.Name + "Option').style.visibility = 'hidden';"

    def setValue(self, inForm: Form):
        return "document.getElementById('" + self.Id + "').value = '" + (inForm.Name if isinstance(inForm, Form)
                                                                         else inForm) + "';"

    def generateDefaultOnChange(self):
        self.setOnChange("for (const option of this.options) { "
                         "document.getElementById(option.value + 'InputForm').style.visibility = 'hidden';};"
                         "document.getElementById(this.value + 'InputForm').style.visibility = 'visible';")
