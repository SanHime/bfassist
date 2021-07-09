#############################################################################
#
#
#   HTML Table webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML table module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        html <- table
         |
         \-> node
          -> tags

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webgen.framework.html.node import HTML_Node
from bfassist.webgen.framework.html.tags import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class TableRow(HTML_Node):
    """ A table row object that should simplify the interactions with table rows.

        :param cells:   A list of cells contained in this row.

            note::  Author(s): Mitch """

    def __init__(self, cells: tuple = None):
        super().__init__('tr')

        if cells:
            self.appendChildNode(cells[0])
            self.cells = cells
        else:
            self.cells = ()

    def __iadd__(self, other):
        """ Helper function to add cells to a row.

            :param other:   Cells to add.

            :return:        The row with the added cells.

                note::  Author(s): Mitch """

        if isinstance(other, HTML_Node):
            self.appendChildNode(other)
            self.cells += (other, )
        elif isinstance(other, tuple) and self.allNodesAreNodes(other):
            self.appendChildrenNodes(other)
            self.cells += other

        return self

    def __iter__(self):
        """ Helper function to make the rows iterable.

            :return:    The iterable of rows.

                note::  Author(s): Mitch """

        return self.cells.__iter__()

    def __getitem__(self, item: int):
        """ Helper function to access cells via their index easily.

            :param item:    The index of the cell that's getting accessed.

            :return:        The cell found at the specified index.

                note:.  Author(s): Mitch """

        return self.cells[item]

    def addCell(self, innerHTML: str = None):
        """ Helper function for adding a single cell.

            :param innerHTML:   The innerHTML of the cell. Should be string for inserting a text but could also be
                                another HTML node.

                note::  Author(s): Mitch """

        newCell = td(innerHTML)
        self.appendChildNode(newCell)
        self.cells += (newCell, )

    def addHeader(self, innerHTML: str = None):
        """ Helper function for adding a single header-cell.

            :param innerHTML:   The innerHTML of the header-cell. Should be string for inserting a text but could also
                                be another HTML node.

                note::  Author(s): Mitch """

        newHeaderCell = th(innerHTML)
        self.appendChildNode(newHeaderCell)
        self.cells += (newHeaderCell, )

    @classmethod
    def fromCellCount(cls, cellCount: int = 1):
        """ Creates a simple table row with the number of cells specified.

            :param cellCount:   The number of cells the row should contain.

                note::  Author(s): Mitch """

        tableRow = cls()
        for x in range(cellCount):
            tableRow.addCell()
        return tableRow

    @classmethod
    def fromHeaderCount(cls, headerCount: int = 1):
        """ Creates a simple table row with the number of header cells specified.

            :param headerCount:   The number of header cells the row should contain.

                note::  Author(s): Mitch """

        tableRow = cls()
        for x in range(headerCount):
            tableRow.addHeader()
        return tableRow


class TableBody(HTML_Node):
    """ A table body object that should simplify the interactions with table bodies.

        :param rows:        A list of rows contained in this table body.
        :param nodeType:    This parameter is necessary so TableHead can inherit from TableBody.

            note::  Author(s): Mitch """

    def __init__(self, rows: tuple = None, nodeType: str = 'tbody'):
        super().__init__(nodeType)

        if rows:
            self.appendChildrenNodes(rows)
            self.rows = rows
        else:
            self.rows = ()

    def __iadd__(self, other):
        """ Helper function to add rows to a body conveniently.

            :return:    This table body with the added row.

                note::  Author(s): Mitch """

        if isinstance(other, TableRow):
            self.appendChildNode(other)
            self.rows += (other, )

        return self

    def __iter__(self):
        """ Helper function to make the rows iterable.

            :return:    The iterable of rows.

                note::  Author(s): Mitch """

        return self.rows.__iter__()

    def __getitem__(self, item: int):
        """ Helper function to access rows via their index easily.

            :param item:    The index of the row that's getting accessed.

            :return:        The row found at the specified index.

                note:.  Author(s): Mitch """

        return self.rows[item]

    def addRowWithColumnCount(self, columnCount: int = 1):
        """ Helper function for adding a single row containing a specified number of columns.

            :param columnCount: The number of columns/cells the row should have

                note::  Author(s): Mitch """

        newRow = TableRow.fromCellCount(columnCount)
        self.appendChildNode(newRow)
        self.rows += (newRow,)

    @classmethod
    def fromRowAndColumnCount(cls, rowCount: int = 1, columnCount: int = 1):
        """ Creates a very simple table body based just on the specification of the number of columns and rows the
        table body should have.

            :param rowCount:    The number of rows of the table body.
            :param columnCount: The number of columns of the table body.

                note::  Author(s): Mitch """

        tableBody = cls()
        for x in range(rowCount):
            tableBody.addRowWithColumnCount(columnCount)
        return tableBody


class TableHead(TableBody):
    """ A table header object that should simplify the interactions with table headers.

        :param rows:    A list of rows contained in this table body.

            note::  Author(s): Mitch """

    def __init__(self, rows: tuple = None):
        super().__init__(rows, 'thead')

    def addRowWithColumnCount(self, columnCount: int = 1):
        """ Helper function for adding a single row containing a specified number of columns.

            :param columnCount: The number of columns/cells the row should have

                note::  Author(s): Mitch """

        newRow = TableRow.fromHeaderCount(columnCount)
        self.appendChildNode(newRow)
        self.rows += (newRow,)

    @classmethod
    def fromRowAndColumnCount(cls, rowCount: int = 1, columnCount: int = 1):
        """ Creates a very simple table body based just on the specification of the number of columns and rows the
        table body should have.

            :param rowCount:    The number of rows of the table body.
            :param columnCount: The number of columns of the table body.

                note::  Author(s): Mitch """

        tableHead = cls()
        for x in range(rowCount):
            tableHead.addRowWithColumnCount(columnCount)
        return tableHead


class Table(HTML_Node):
    """ A table object that should simplify the interactions with tables.

        :param tableHeaders:    The table header elements of this table.
        :param tableBodies:     The table body elements of this table.
        :param tableFooters:    The table footer elements of this table.

        :param rows:            The rows of a table consist only of the rows in the table bodies concatenated together.

            note::  Author(s): Mitch """

    def __init__(self, tableHeaders: tuple = None, tableBodies: tuple = None, tableFooters: tuple = None,
                 rows: tuple = None):
        super().__init__('table')

        if tableHeaders:
            self.appendChildNode(tableHeaders[0])
            self.tableHeaders = tableHeaders
        else:
            self.tableHeaders = ()

        if tableBodies:
            self.appendChildNode(tableBodies[0])
            self.tableBodies = tableBodies
        else:
            self.tableBodies = ()

        if tableFooters:
            self.appendChildNode(tableFooters[0])
            self.tableFooters = tableFooters
        else:
            self.tableFooters = ()

        if rows:
            self.rows = rows
        else:
            self.rows = ()
            if self.tableBodies:
                for tableBody in self.tableBodies:
                    self.rows += tableBody.rows

    @classmethod
    def fromRowAndColumnCount(cls, rowCount: int = 1, columnCount: int = 1):
        """ Creates a very simple table based just on the specification of the number of columns and rows the table
        should have.

            :param rowCount:    The number of rows of the table.
            :param columnCount: The number of columns of the table.

                note::  Author(s): Mitch """

        tableBody = TableBody.fromRowAndColumnCount(rowCount, columnCount)
        return cls(tableBodies=(tableBody,))

    def __iter__(self):
        """ Helper function to make the rows iterable.

            :return:    The iterable of rows.

                note::  Author(s): Mitch """

        return self.rows.__iter__()

    def __getitem__(self, item: int):
        """ Helper function to access rows via their index easily.

            :param item:    The index of the row that's getting accessed.

            :return:        The row found at the specified index.

                note:.  Author(s): Mitch """

        return self.rows[item]
