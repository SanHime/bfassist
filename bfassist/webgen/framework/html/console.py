#############################################################################
#
#
#   HTML console webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML bfa api console module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining
the webclient of bfa.

    Dependencies:

        bfassist <- (webgen.)framework <- html <- console
            |                   |        |
            |                   |        |-> node
            |                   |        |-> table
            |                   |        |-> output
            |                   |        |-> scrolltable
            |                   |        |-> form
            |                   \        \-> tags
            \                    -> css
             -> api @Console.installAPI

        note::  Author(s): Mitch last-check: 07.07.2021 """

from copy import deepcopy

from bfassist.webgen.framework.html.node import HTML_Node
from bfassist.webgen.framework.html.table import Table
from bfassist.webgen.framework.html.output import TextArea
from bfassist.webgen.framework.html.scrolltable import ScrollTable
from bfassist.webgen.framework.html.form import Form
from bfassist.webgen.framework.html.tags import h4
from bfassist.webgen.framework.css import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class Console(HTML_Node):
    """ A console object that should simplify the interactions with consoles for bfa apis. This object is actually a div
    container wrapping the console.

        :param Name:        Name of this console, should be unique among consoles of the same document because it's part
                            of its id.
        :param ConsoleAPI:  The bfa api dictionary this console should serve.
        :param LayoutTable: The layout table that defines the layout of the console, by default consisting of a single
                            row with two cells.
        :param InputPort:   The input port of this console, by default the right cell of the layout table.
        :param OutputPort:  The output port of this console, by default the left cell of the layout table.
        :param Input:       The actual input of the console, by default a scroll table.
        :param Output:      The actual output of the console, by default a textarea.
        :param styles:      A set of CSS rules that define styles for this console.
        :param script:      A tuple of JS functions for this console.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, ConsoleAPI: dict = None, LayoutTable: Table = None, InputPort: HTML_Node = None,
                 OutputPort: HTML_Node = None, Input: HTML_Node = None, Output: HTML_Node = None, styles: set = None,
                 script: tuple = None):

        self.Name = Name
        if ConsoleAPI:
            self.ConsoleAPI = ConsoleAPI
        else:
            self.ConsoleAPI = {}
        super().__init__('div', Id=self.Name + 'ConsoleWrapper', Class='consoleWrapper')
        if LayoutTable:
            self.LayoutTable = LayoutTable
            self.appendChildNode(self.LayoutTable)
        else:
            self.LayoutTable = Table.fromRowAndColumnCount(1, 2)
            self.LayoutTable.Id = self.Name + 'ConsoleLayoutTable'
            self.LayoutTable.Class = 'consoleLayoutTable'
            self.appendChildNode(self.LayoutTable)
        if InputPort:
            self.InputPort = InputPort
        else:
            self.InputPort = self.LayoutTable[0][0]
            self.InputPort.Id = self.Name + 'ConsoleInputPort'
            self.InputPort.Class = 'consoleInputPort'
        if OutputPort:
            self.OutputPort = OutputPort
        else:
            self.OutputPort = self.LayoutTable[0][1]
            self.OutputPort.Id = self.Name + 'ConsoleOutputPort'
            self.OutputPort.Class = 'consoleOutputPort'
        if Input:
            self.Input = Input
            self.InputPort.appendChildNode(self.Input)
        else:
            self.Input = ScrollTable(self.Name + 'Input')
            self.InputPort.appendChildNode(self.Input)
        if Output:
            self.Output = Output
            self.OutputPort.appendChildNode(self.Output)
        else:
            self.Output = TextArea()
            self.Output.Id = self.Name + 'ConsoleOutput'
            self.Output.Class = 'consoleOutput'
            self.OutputPort.appendChildNode(self.Output)
        if styles:
            self.styles = styles
        else:
            self.styles = set()
        if script:
            self.script = script
        else:
            self.script = ()

        self.styles.update({self.styleConsole(), self.Input.getStandardStyle(),
                            self.styleOutputPort(), self.styleOutput()})

        self.installAPI()

    def installAPI(self, consoleAPI: dict = None):
        from bfassist.api import getFunctions

        consoleAPI = deepcopy(consoleAPI)
        if consoleAPI:
            self.ConsoleAPI = consoleAPI
        for apiF in getFunctions(self.ConsoleAPI):
            form = Form.createInputFormForFunction(apiF, self.Output)
            self.Input.appendRow((
                h4(apiF.name),
                form
            ))
            self.script += form.script

    def setInputMaxHeight(self, maxHeight: str):
        self.styles.add(self.Input.setMaxHeight(maxHeight))

    def setOutputHeight(self, height: str):
        self.styles.add(self.Output.styleThisNode({
            set_height(height)
        }))

    def setHeight(self, height: str):
        self.setInputMaxHeight(height)
        self.setOutputHeight(height)

    def setInputBorderColour(self, colour: RGB_Colour):
        self.styles.add(self.Input.setBorderColour(colour))

    def styleConsole(self):
        return self.styleThisNode({
            set_width('100%'),
            set_height('100%')
        })

    def styleOutput(self):
        return self.Output.styleThisNode({
            set_width('99%'),
            set_border_radius('10px')
        })

    def styleOutputPort(self):
        return self.OutputPort.styleThisClass({
            set_width('57%'),
            set_height('100%')
        })
