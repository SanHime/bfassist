#############################################################################
#
#
#   HTML scroll table webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML scroll table module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        bfassist <- (webgen.)framework <- html <- scrolltable
            |                   |           |
            |                   |           |-> node
            |                   |           \-> tags
            |                   |            -> table
            |                   \-> css
            \                    -> js -> xmlhttp
             -> colours

        note::  Author(s): Mitch last-check: 07.07.2021 """

from copy import deepcopy

from bfassist.webgen.framework.html.node import HTML_Node
from bfassist.webgen.framework.html.tags import *
from bfassist.webgen.framework.html.table import *
from bfassist.webgen.framework.css import *
from bfassist.webgen.framework.js import *
from bfassist.webgen.framework.js.xmlhttp import *
from bfassist.colours import RGBA_Colour


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class ScrollTable(HTML_Node):
    """ A scroll table object that should simplify the interactions with scroll tables. This object is not actually the
     table object itself but the div container wrapping the table.

        :param Name:            Name of this table, should be unique among scroll tables of the same document because
                                it's part of its id.
        :param Heading:         Will add a heading above the table if specified.
        :param dataHint:        Data hint containing information what and how to display data in this table. For example
                                the return type hint of an api function
        :param dataFunctions:   A tuple of functions that can use data from this scroll table.
        :param constraint:      A set containing the attribute names from the displayHint that should actually be
                                displayed.
        :param displayHint:     The "intersection" of dataHints and constraint containing only the hints used.
        :param styles:          A set of CSS rules that define styles for this scroll table.
        :param script:          A tuple of JS functions for this scroll table.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, Heading: str = None, dataHint: dict = None, dataFunctions: tuple = None,
                 constraint: set = None, displayHint: dict = None, styles: set = None, script: tuple = None):
        self.Name = Name
        super().__init__('div', Id=self.Name + 'ScrollTableWrapper', Class='scrollTableWrapper')

        if Heading:
            self.Heading = h2(Heading)
            self.innerHTML += (self.Heading, )

        if isinstance(dataHint, list):
            self.dataHint = dataHint[0]
        else:
            self.dataHint = dataHint
        if dataFunctions:
            self.dataFunctions = dataFunctions
        else:
            self.dataFunctions = ()
        self.constraint = constraint

        if displayHint:
            self.displayHint = displayHint
        else:
            self.displayHint = deepcopy(self.dataHint)

        if styles:
            self.styles = styles
        else:
            self.styles = set()

        if script:
            self.script = script
        else:
            self.script = ()

        if self.dataHint:
            self.intersectDataHintsWithConstraint()
            tableHead = self.constructHeadFromDataHint()
            tableBody = self.constructBody()
            actualTable = self.constructTable(tableHead, tableBody)
            self.innerHTML += (actualTable, )
            self.script += (self.extractDataFromRow(), self.getScriptForClickingDataRows(),
                            self.getScriptForFillingScrollTablesUsingCellContentWrappers())
        else:
            self.innerHTML += (Table(tableBodies=(TableBody(), )), )

    def intersectDataHintsWithConstraint(self):
        """ Constraints the display hints by removing data hints that are not contained in the constraint actually used.

                note::  Author(s): Mitch """
        if self.constraint is None:
            return
        else:
            for hint in self.dataHint:
                if hint not in self.constraint:
                    self.displayHint.pop(hint)

    def constructTable(self, tableHead: TableHead, tableBody: TableBody):
        """ Constructs the table.

            :param tableHead:   The table head of the table.
            :param tableBody:   The table body of the table.

            :return:    The table.

                note::  Author(s): Mitch """

        actualTable = Table((tableHead,), (tableBody,))
        actualTable.Id = self.Name + 'ScrollTable'
        actualTable.Class = "scrollTable"
        return actualTable

    def constructBody(self):
        """ Constructs the table body element.

            :return:    The table body.

                note::  Author(s): Mitch """

        tableBody = TableBody()
        tableBody.Id = self.Name + 'ScrollTableBody'
        tableBody.Class = 'scrollTableBody'
        self.styles.add(tableBody.styleThisNode({
            set_max_height('150px')
        }))
        return tableBody

    def constructHeadFromDataHint(self):
        """ Constructs the table head element from the data hint dictionary.

            :return:    The table head.

                note::  Author(s): Mitch """
        tableHead = TableHead.fromRowAndColumnCount(1, len(self.displayHint))
        tableHead[0].Id = self.Name + 'ScrollTableHead'
        tableHead[0].Class = 'scrollTableHead'

        displayHints = list(self.displayHint.keys())
        for x in range(len(displayHints)):
            tableHeader = tableHead[0][x]
            tableHeader.properties['class'] = 'scrollTableHeader'
            tableHeader.innerHTML = displayHints[x]

        self.styles.add(tableHead[0].styleThisNodesSubType('th', {
            set_width('{:.2%}'.format(1 / len(self.displayHint)))
        }))

        return tableHead

    def defineStyleForDataCells(self, borderColour: RGBA_Colour):
        """ Function to define style for the data cells which will be created by the associated JS script.

            :param borderColour:    The colour to use for the border of the data cells.

                note::  Author(s): Mitch """

        self.styles.add(CSS_Style('tbody#' + self.Name + 'ScrollTableBody td.scrollTableCell', {
            set_width('{:.2%}'.format(1/len(self.displayHint))),
            set_border('2px', 'solid', borderColour),
            set_overflow('hidden')
        }))

    def getStandardStyle(self):
        """ This function returns the standard style for a scroll table.

                note::  Author(s): Mitch """

        return self.styleThisNode({
            set_overflowY('scroll'),
            set_display('block'),
            set_border_radius('5px')
        })

    def setMaxHeight(self, maxHeight: str):
        return self.styleThisNode({
            set_max_height(maxHeight)
        })

    def setBorderColour(self, colour: RGB_Colour):
        return self.styleThisNode({
            set_border('2px', 'solid', colour)
        })

    @staticmethod
    def getTableStyle():
        return CSS_Style('table.scrollTable', {
            set_width('100%')
        })

    @staticmethod
    def getTableBodyClassStyle():
        return CSS_Style('tbody.scrollTableBody', {
            set_display('block'),
            set_width('100%'),
            set_overflowY('scroll'),
            set_height('auto'),
            set_border_collapse('collapse')
        })

    @staticmethod
    def getTableHeadStyle():
        return CSS_Style('tr.scrollTableHead', {
            set_display('flex')
        })

    @staticmethod
    def getTableHeaderStyle(bottomBorderColour: RGB_Colour, borderColour: RGB_Colour):
        return CSS_Style('th.scrollTableHeader', {
            set_flex('1', 'auto'),
            set_display('block'),
            set_border_bottom('1px', 'solid', bottomBorderColour),
            set_border_left('1px', 'solid', borderColour),
            set_border_right('1px', 'solid', borderColour),
            set_border_radius('4px'),
            set_overflowX('hidden')
        })

    @staticmethod
    def getScrollTableClassStyle():
        return CSS_Style('.scrollTable ::after', {
            set_content("''"),
            set_overflowY('scroll'),
            set_visibility('hidden')
        })

    @staticmethod
    def getScrollTableRowClassStyle():
        return CSS_Style('.scrollTableRow', {
            set_height('24px')
        })

    @staticmethod
    def getClickedScrollTableRowClassStyle(clickedColour: RGB_Colour):
        return CSS_Style('.clickedScrollTableRow', {
            set_background_colour(clickedColour)
        })

    @staticmethod
    def getScrollTableRowCellContentWrapperClassStyle():
        return CSS_Style('.scrollTableCellContentWrapper', {
            set_white_space('nowrap'),
            set_width('0px')
        })

    @staticmethod
    def getAllScrollTableStyles(bottomBorderColour: RGB_Colour, borderColour: RGB_Colour, clickedColour: RGB_Colour):
        CSS = set()
        CSS.add(ScrollTable.getTableStyle())
        CSS.add(ScrollTable.getTableBodyClassStyle())
        CSS.add(ScrollTable.getTableHeadStyle())
        CSS.add(ScrollTable.getTableHeaderStyle(bottomBorderColour, borderColour))
        CSS.add(ScrollTable.getScrollTableClassStyle())
        CSS.add(ScrollTable.getScrollTableRowClassStyle())
        CSS.add(ScrollTable.getClickedScrollTableRowClassStyle(clickedColour))
        CSS.add(ScrollTable.getScrollTableRowCellContentWrapperClassStyle())
        return CSS

    def getScriptForClickingDataRows(self):
        code = JS_Function_Body()
        code += "if ('clickedScrollTableRow' === this.className) {\n" \
                "\tthis.classList.remove('clickedScrollTableRow')\n" \
                "}\n" \
                "else {\n" \
                "\tlet clicked = this.parentElement.getElementsByClassName('clickedScrollTableRow')\n" \
                "\tfor (const row of clicked) {\n" \
                "\t\trow.classList.remove('clickedScrollTableRow')\n" \
                "\t}\n" \
                "\tthis.classList.add('clickedScrollTableRow')\n" \
                "\tdata = " + self.Name + "getDataFromRow(this)\n" \
                "}\n"
        for func in self.dataFunctions:
            code += func.name + "FillFormWithData(data)\n"
        return JS_Function(self.Name + 'RowClick', body=code)

    def extractDataFromRow(self):
        code = JS_Function_Body()
        code += "let data = []\n" \
                "for (const dat of dataRow.cells){\n" \
                "\tdata.push(dat.children[0].innerHTML)\n" \
                "}\n" \
                "let annotated_data = {}\n"

        displayHints = list(self.displayHint.keys())
        for x in range(len(displayHints)):
            code += "annotated_data['" + displayHints[x] + "'] = data[" + str(x) + "]\n"
        code += "return annotated_data"
        return JS_Function(self.Name + 'getDataFromRow', parameters=('dataRow', ), body=code)

    def getScriptForFillingScrollTablesUsingCellContentWrappers(self):
        return JS_Function(self.Name + 'FillScrollTable', parameters=('input', ), body=JS_Function_Body(
            "for (const row_data of input) {\n"
            "\trow = document.getElementById('" + self.Name + "ScrollTable').tBodies[0].insertRow(-1)\n"
            "\trow.onclick = " + self.getScriptForClickingDataRows().name + "\n"
            "\tfor (const cell_data of row_data) {\n"
            "\t\tlet cell = row.insertCell(-1)\n"
            "\t\tcell.innerHTML = '<div class=\\'scrollTableCellContentWrapper\\'>' + cell_data + '</div>'\n"
            "\t\tcell.classList.add('scrollTableCell')\n"
            "\t}\n"
            "}\n"
        ))

    @staticmethod
    def getScriptForClearingScrollTable():
        return JS_Function('clearScrollTable', parameters=('scrollTable',), body=JS_Function_Body(
            "var old_tbody = scrollTable.tBodies[0]\n"
            "var new_tbody = document.createElement('tbody')\n"
            "new_tbody.id = old_tbody.id\n"
            "new_tbody.className = old_tbody.className\n"
            "scrollTable.replaceChild(new_tbody, old_tbody)\n"
        ))

    @staticmethod
    def getScriptForClearingScrollTables():
        return JS_Function('clearScrollTables', body=JS_Function_Body(
            "var scrollTables = document.getElementsByClassName('scrollTable')\n"
            "for (const scrollTable of scrollTables) {\n"
            "\t" + ScrollTable.getScriptForClearingScrollTable().call() + "\n"
            "}\n"
        ))

    def getPostProcessingForRequestDataForThisScrollTable(self):
        """ Yields a post processing function body for the post procession of a successful api request for the data that
        is supposed to be displayed in this scroll table.

            :return:    JS request procession function that handles post processing for data from an api request to be
                        displayed in this scroll table.

                note::  Author(s): Mitch """
        js = JS_Function_Body(
            "let results = []\n"
            "for (const result_data of xmlhttp.response){\n"
            "\tvar result = []\n"
        )
        for hint in self.displayHint:
            if isinstance(self.displayHint[hint], dict):
                for dictHint in self.displayHint[hint]:
                    js += "\tresult.push(result_data['" + hint + "']['" + dictHint + "'])\n"
            else:
                js += "\tresult.push(result_data['" + hint + "'])\n"

        js += "\tresults.push(result)\n" \
              "}\n" + \
              self.Name + "FillScrollTable(results)\n"

        return RequestPostProcessing(js)

    @staticmethod
    def enableScrollTableRowClick():
        return "document.getElementsByClassName('scrollTableRow').onclick = rowClick;"

    def appendRow(self, innerHTML: tuple):
        """ This functions appends a single row containing a single cell and returns the cell at the end.

            :param innerHTML:   Inner HTML to be set for the cell.

                note::  Author(s): Mitch """

        row = TableRow.fromCellCount(1)
        row.Class = 'scrollTableRow'
        cell = row[0]
        cell.Class = 'scrollTableCell'
        cell.innerHTML = innerHTML
        self.table.tableBodies[0].appendChildNode(row)
