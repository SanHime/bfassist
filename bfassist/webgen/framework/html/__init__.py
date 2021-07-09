#############################################################################
#
#
#   HTML Document webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the webclient of
bfa. Most importantly this module contains the HTML document class and makes elements of sub-modules available.

    Dependencies:

        html -----> node
                |-> head
                |-> body
                |-> tags
                |-> table
                |-> output
                |-> userinput
                \-> form
                |-> scrolltable
                |-> inputport
                 -> console

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webgen.framework.html.node import HTML_Node, HTML_Node_Contentless
from bfassist.webgen.framework.html.head import HTML_Head
from bfassist.webgen.framework.html.body import HTML_Body
from bfassist.webgen.framework.html.tags import *
from bfassist.webgen.framework.html.table import *
from bfassist.webgen.framework.html.output import *
from bfassist.webgen.framework.html.userinput import *
from bfassist.webgen.framework.html.form import *
from bfassist.webgen.framework.html.scrolltable import *
from bfassist.webgen.framework.html.inputport import *
from bfassist.webgen.framework.html.console import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class HTML_Document(HTML_Node):
    """ HTML Document representation.

        :param filename:    Filename of the document.
        :param lang:        Language the document is written in.
        :param Head:        HTML header of the document.
        :param Body:        HTML body of the document.

        :param charset: Charset used in the document as specified in the header.

            note::  Author(s): Mitch """

    def __init__(self, nodeType: str = "html", filename: str = "index.html", lang: str = "en", Head: HTML_Head = None,
                 Body: HTML_Body = None):

        self.filename = filename
        self.lang = lang

        if Head is None:
            self.head = HTML_Head()
        elif isinstance(Head, HTML_Head):
            self.head = Head
        else:
            raise TypeError("Parameter Head has to be an HTML header!")

        if Body is None:
            self.body = HTML_Body()
        elif isinstance(Body, HTML_Body):
            self.body = Body
        else:
            raise TypeError("Parameter Body has to be an HTML body!")
        super().__init__(nodeType, properties={'lang': 'en'}, innerHTML=(self.head, self.body))
        self.charset = self.getCharset()

    def setTitle(self, title: str):
        """ Simple function to set the title of the HTML document.

            :param title:   The title of the HTML document.

                note::  Author(s): Mitch """

        self.head.title = title

    def getCharset(self):
        """ Charset of this document.

            :return:    Charset.

                note::  Author(s): Mitch """

        return self.head.getCharset()

    def toString(self):
        """ Converts the document to a string with the encoding specified in the meta-data.

            :return:    Document as string.

                note::  Author(s): Mitch """

        doc = "<!DOCTYPE html>\n" + super().toString()

        return doc

    def addStyleSheet(self, stylesheet: HTML_Node_Contentless):
        """ Adds a stylesheet link to the header of this document.

            :param stylesheet:  The stylesheet as link node.

                note::  Author(s): Mitch """

        self.head.addStyleSheet(stylesheet)

    def addScript(self, script: HTML_Node):
        """ Adds a script to the header of this document.

            :param script:  The script as script node.

                note::  Author(s): Mitch """

        self.head.addScript(script)

    def appendChildNode(self, child: HTML_Node):
        self.body.appendChildNode(child)

    def appendChildrenNodes(self, children: tuple):
        self.body.appendChildrenNodes(children)
