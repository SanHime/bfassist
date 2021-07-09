#############################################################################
#
#
#   webGen framework HTML output module to BFA v.5 standalone
#
#
#############################################################################
""" Module to improve python to HTML coding with the bfa webGen modules.

    Dependencies:

        output
         |
         v
        node

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webgen.framework.html.node import HTML_Node


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Output(HTML_Node):
    """ An output object that should simplify the interactions with outputs.

            note::  Author(s): Mitch """

    def __init__(self, nodeType: str):
        super().__init__(nodeType)

    def assign(self, value: str):
        return "document.getElementById('" + self.Id + "').innerHTML = " + value

    def write(self, output: str):
        return "document.getElementById('" + self.Id + "').innerHTML = '" + output + "'"

    def append(self, appendage: str):
        return "document.getElementById('" + self.Id + "').innerHTML += '" + appendage + "'"


class SimpleOutput(Output):
    """ The most simple output form, just a div container to write to.

            note::  Author(s): Mitch """

    def __init__(self):
        super().__init__('div')


class TextArea(Output):
    """ A textarea output for large size output.

            note::  Author(s): Mitch """

    def __init__(self):
        super().__init__('textarea')
