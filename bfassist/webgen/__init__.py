#############################################################################
#
#
#   webGen module to BFA c7
#
#
#############################################################################
""" This is a simple HTML/JS/CSS generator/framework mainly for the purpose of maintaining the webclient of bfa.
It's borrowing some ideas from the model-view-presenter scheme to produce 'views' containing html, css, js.
This package is still under heavy-development and will continue to change a lot. The next concept that should be
integrated is that of 'subviews', not actually served from the webservice on their own but, that can concatenate
together to produce 'views' actually served from the webservice.

    Dependencies:

        webgen -> framework

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations

from os.path import exists

from bfassist.webgen.framework import *
from bfassist.webgen.framework.html import HTML_Node
from bfassist.webgen.framework.css import CSS_Style
from bfassist.webgen.framework.js import JS_Function


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class View:
    """ Represents a specific view from the browser at the webclient.

        :param Name:            Name and importantly also the name of the folder/package that's used for production.
        :param DisplayName:     Name of the view when displayed e.g. in the navigation.
        :param Description:     A description of this view.

        :param HTML_DOCUMENT:   HTML document to produce this view.
        :param STYLE_SHEET:     "Private" CSS style sheet of this view.
        :param SCRIPT:          "Private" JS script of this view.
        :param Stylesheets:     Dictionary of stylesheets used in this view with the view the stylesheets originally
                                belong to as keys.
        :param Scripts:         Dictionary of scripts used in this view with names as keys.

        :param cached:          A cached version of the view. A list containing the html, css and js.
        :param exported:        An exported version of the view. A list containing the paths to the html, css and js.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, DisplayName: str, Description: str = "",
                 HTML_DOCUMENT: HTML_Document = None, STYLE_SHEET: CSS_Stylesheet = None, SCRIPT: JS_Script = None,
                 Stylesheets: dict = None, Scripts: dict = None, cached: list = None, exported: list = None):

        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description

        if HTML_DOCUMENT is None:
            self.HTML_DOCUMENT = HTML_Document()
        else:
            self.HTML_DOCUMENT = HTML_DOCUMENT

        if STYLE_SHEET is None:
            self.STYLE_SHEET = CSS_Stylesheet(self.Name + 'Styles.css')
        else:
            self.STYLE_SHEET = STYLE_SHEET

        if SCRIPT is None:
            self.SCRIPT = JS_Script(self.Name + 'Script.js')
        else:
            self.SCRIPT = SCRIPT

        if Stylesheets is None:
            self.Stylesheets = {self: self.STYLE_SHEET}
        else:
            self.Stylesheets = Stylesheets

        for view in self.Stylesheets:
            if view == self:
                self.HTML_DOCUMENT.addStyleSheet(self.styleSheetToNode())
            else:
                self.addScriptFromForeignView(view)

        if Scripts is None:
            self.Scripts = {self: self.SCRIPT}
        else:
            self.Scripts = Scripts

        for view in self.Scripts:
            if view == self:
                self.HTML_DOCUMENT.addScript(self.scripToNode())
            else:
                self.addScriptFromForeignView(view)

        self.cached = cached
        self.exported = exported

    def setTitle(self, title: str):
        self.HTML_DOCUMENT.setTitle(title)

    def __iadd__(self, other):
        """ Truly magic function that can receive a single HTML_Node, CSS_Style or JS_Function and correctly append it
        to the HTML, CSS or JS of this view. It can also receive tuples of valid inner HTML or JS functions as well as
        sets of CSS styles and even tuples containing 3 of these in a random order.

            :param other:   Value as specified in the description.

            :return:        The return value of the respective __iadd__ called.

                note::  Author(s): Mitch """

        if isinstance(other, HTML_Node):
            self.HTML_DOCUMENT.__iadd__(other)
            return self
        elif isinstance(other, CSS_Style):
            self.STYLE_SHEET.__iadd__(other)
            return self
        elif isinstance(other, JS_Function):
            self.SCRIPT.__iadd__(other)
            return self
        elif isinstance(other, tuple):
            if HTML_Node.isValidInnerHTML(other):
                self.HTML_DOCUMENT.__iadd__(other)
                return self
            elif JS_Script.allFunctionsAreFunctions(other):
                self.SCRIPT.__iadd__(other)
                return self
            else:
                if 1 <= len(other) <= 3:
                    try:
                        for elem in other:
                            self.__iadd__(elem)
                        return self
                    except TypeError:
                        raise TypeError("Can only += tuples containing HTML_Node, CSS_Style, JS_Function or tuples"
                                        "containing tuples of valid inner HTML or exclusively JS functions or sets of"
                                        "CSS styles. But " + str(other) + " is not.")
                else:
                    raise TypeError("Can only += tuples with valid innerHTML or containing only JS_Function but " +
                                    str(other) + " is neither.")
        elif isinstance(other, set):
            if CSS_Stylesheet.allStylesAreStyles(other):
                self.STYLE_SHEET.__iadd__(other)
                return self
            else:
                raise TypeError("Can only += sets containing only CSS_Style but " + str(other) + " is not.")
        else:
            raise TypeError("Can only += values of type HTML_Node, CSS_Style or JS_Function but value was of type " +
                            str(type(other)))

    @staticmethod
    def build():
        """ Function to be overridden for building the view so its code can be read after the rest of the application
        was loaded.

                note::  Author(s): Mitch """

        pass

    def styleSheetToNode(self):
        """ Function to turn the style sheet of this view into a node for linking it in the head of its HTML document.

            :return:    The node that links to the style sheet.

                note::  Author(s): Mitch """

        return self.STYLE_SHEET.toNode(self.Name + '/' + self.STYLE_SHEET.filename)

    def asForeignStyleSheetToNode(self, foreignView: View):
        """ Function to turn the sheet of this view into a node for a foreign view.

            :param foreignView: The foreign view that wants to link this style sheet.

            :return:            The node links to the style sheet.

                note::  Author(s): Mitch """

        depth = foreignView.Name.count('/') + 1
        return self.STYLE_SHEET.toNode('../'*depth + self.Name + '/' + self.STYLE_SHEET.filename)

    def addStyleSheetFromForeignView(self, foreignView: View):
        """ Function to add a foreign stylesheet to this view.

            :param foreignView: The view to add the stylesheet from.

                note::  Author(s): Mitch """

        self.Stylesheets[foreignView] = foreignView.STYLE_SHEET
        self.HTML_DOCUMENT.addStyleSheet(foreignView.asForeignStyleSheetToNode(self))

    def scripToNode(self):
        """ Function to turn the script of this view into a node for linking it in the head of a HTML document.

            :return:    The node that links to the script.

                note::  Author(s): Mitch """

        return self.SCRIPT.toNode(self.Name + '/' + self.SCRIPT.filename)

    def asForeignScriptToNode(self, foreignView: View):
        """ Function to turn the script of this view into a node for a foreign view.

            :param foreignView: The foreign view that wants to link this script.

            :return:            The node links to the script.

                note::  Author(s): Mitch """

        depth = foreignView.Name.count('/') + 1
        return self.SCRIPT.toNode('../' * depth + self.Name + '/' + self.SCRIPT.filename)

    def addScriptFromForeignView(self, foreignView: View):
        """ Function to add a foreign already exported script to this view.

            :param foreignView: The view to add the script from.

                note::  Author(s): Mitch """

        self.Scripts[foreignView] = foreignView.SCRIPT
        self.HTML_DOCUMENT.addScript(foreignView.asForeignScriptToNode(self))

    def exportHTML(self):
        """ Function to export the HTML document of this view.

                note::  Author(s): Mitch """

        with open('bfassist/standalone/webclient/' + self.Name + '/' + self.HTML_DOCUMENT.filename, 'w') as htmlFile:
            htmlFile.write(self.HTML_DOCUMENT.toString())

    def exportStyleSheet(self):
        """ Function to export the stylesheets attached to this view.

                note::  Author(s): Mitch """

        with open('bfassist/standalone/webclient/' + self.Name + '/' + self.STYLE_SHEET.filename, 'w') as cssFile:
            cssFile.write(self.STYLE_SHEET.toString())

    def exportScript(self):
        """ Function to export the scripts attached to this view.

                note::  Author(s): Mitch """

        with open('bfassist/standalone/webclient/' + self.Name + '/' + self.SCRIPT.filename, 'w') as jsFile:
            jsFile.write(self.SCRIPT.toString())

    def export(self):
        """ Function to export all documents attached to this view.

                note::  Author(s): Mitch """

        try:
            if not exists('bfassist/standalone/webclient/' + self.Name + '/' + self.HTML_DOCUMENT.filename):
                self.exportHTML()
            else:
                with open('bfassist/standalone/webclient/' + self.Name + '/' + self.HTML_DOCUMENT.filename, 'r') \
                        as htmlFile:
                    HTML = htmlFile.read()
                    if len(HTML) != len(self.HTML_DOCUMENT.toString()):
                        self.exportHTML()

            if self.exported:
                self.exported[0] = 'bfassist/standalone/webclient/' + self.Name + '/' + self.HTML_DOCUMENT.filename
            else:
                self.exported = ['bfassist/standalone/webclient/' + self.Name + '/' + self.HTML_DOCUMENT.filename, None,
                                 None]

            if not exists('bfassist/standalone/webclient/' + self.Name + '/' + self.STYLE_SHEET.filename):
                self.exportStyleSheet()
            else:
                with open('bfassist/standalone/webclient/' + self.Name + '/' + self.STYLE_SHEET.filename, 'r') \
                        as cssFile:
                    CSS = cssFile.read()
                    if len(CSS) != len(self.STYLE_SHEET.toString()):
                        self.exportStyleSheet()

            if self.exported:
                self.exported[1] = 'bfassist/standalone/webclient/' + self.Name + '/' + self.STYLE_SHEET.filename
            else:
                self.exported = [None, 'bfassist/standalone/webclient/' + self.Name + '/' + self.STYLE_SHEET.filename,
                                 None]

            if not exists('bfassist/standalone/webclient/' + self.Name + '/' + self.SCRIPT.filename):
                self.exportScript()
            else:
                with open('bfassist/standalone/webclient/' + self.Name + '/' + self.SCRIPT.filename, 'r') as jsFile:
                    JS = jsFile.read()
                    if len(JS) != len(self.SCRIPT.toString()):
                        self.exportScript()

            if self.exported:
                self.exported[2] = 'bfassist/standalone/webclient/' + self.Name + '/' + self.SCRIPT.filename
            else:
                self.exported = [None, None, 'bfassist/standalone/webclient/' + self.Name + '/' + self.SCRIPT.filename]

        except FileNotFoundError:
            print("Using module outside of valid bfa environment. Commencing without exporting the " +
                  self.DisplayName + " view.")

    def cacheExported(self):
        """ Function to cache the exported documents of this view.

                note::  Author(s): Mitch """

        with open(self.exported[0], 'r') as htmlFile:
            HTML = htmlFile.read()
        with open(self.exported[1], 'r') as cssFile:
            CSS = cssFile.read()
        with open(self.exported[2], 'r') as jsFile:
            JS = jsFile.read()

        self.cached = [HTML, CSS, JS]

    def serveHTML(self):
        """ Function to serve the HTML document of this view.

            :return:    The HTML document of this view as string.

                note::  Author(s): Mitch """

        if self.cached:
            return self.cached[0]
        elif self.exported:
            self.cacheExported()
        else:
            self.export()
            self.cacheExported()
        return self.serveHTML()

    def serveCSS(self):
        """ Function to serve the CSS stylesheet of this view.

            :return:    The CSS stylesheet of this view as string.

                note::  Author(s): Mitch """

        if self.cached:
            return self.cached[1]
        elif self.exported:
            self.cacheExported()
        else:
            self.export()
            self.cacheExported()
        return self.serveCSS()

    def serveJS(self):
        """ Function to serve the JS script of this view.

            :return:    The JS script of this view as string.

                note::  Author(s): Mitch """

        if self.cached:
            return self.cached[2]
        elif self.exported:
            self.cacheExported()
        else:
            self.export()
            self.cacheExported()
        return self.serveJS()
