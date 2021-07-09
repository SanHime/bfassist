#############################################################################
#
#
#   HTML Head webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML head module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        head
         |
         v
        node

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webgen.framework.html.node import HTML_Node, HTML_Node_Contentless


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class HTML_Head(HTML_Node):
    """ Representation of the HTML header.

        :param meta:    Meta data for this HTML document as tuple(immutable list).
        :param title:   Title of this document.
        :param links:   Stylesheet links.
        :param scripts: Scripts used.

            note::  Author(s): Mitch """

    def __init__(self, nodeType: str = 'head', meta: tuple = None, title: HTML_Node = None, links: tuple = (),
                 scripts: tuple = ()):

        if meta is None:
            self.meta = (HTML_Node_Contentless('meta', properties={'charset': 'utf-8'}),)
        elif self.allNodesAreContentless(meta):
            self.meta = meta
        else:
            raise TypeError("All elements of parameter meta have to be contentless HTML nodes!")

        if title is None:
            self.title = HTML_Node('title')
        elif isinstance(title, HTML_Node):
            self.title = title
        else:
            raise TypeError("Parameter title has to be an HTML node.")

        if self.allNodesAreContentless(links):
            self.links = links
        else:
            raise TypeError("All elements of parameter links have to be contentless HTML nodes!")

        if self.allNodesAreNodes(scripts):
            self.scripts = scripts
        else:
            raise TypeError("All elements of parameter scripts have to be HTML nodes!")

        super().__init__(nodeType, innerHTML=self.meta + (self.title,) + self.links + self.scripts)

    def getCharset(self):
        """ Finds the charset for this document from the meta data tags.

            :return:    Charset for this HTML document.

                note:: Author(s): Mitch """

        for node in self.meta:
            if isinstance(node, HTML_Node_Contentless) and 'charset' in node.properties:
                return node.properties['charset']

    @property
    def title(self):
        """ Gets the title specified in this HTML header.

            :return:    Title specified.

                    note::  Author(s): Mitch """
        return self._title

    @title.setter
    def title(self, title: str):
        """ Sets the title of this HTML header.

            :param title:   Title to be set either string or node.

                note::  Author(s): Mitch """

        if isinstance(title, str):
            self._title.innerHTML = (title,)
        elif isinstance(title, HTML_Node):
            self._title = title
        else:
            raise ValueError("A title has to be a string or a node.")

    def addStyleSheet(self, stylesheet: HTML_Node_Contentless):
        """ Adds a stylesheet link to this header.

            :param stylesheet:  The stylesheet as link node.

                note::  Author(s): Mitch """

        self.links += (stylesheet,)
        self.innerHTML += (stylesheet,)

    def addScript(self, script: HTML_Node):
        """ Adds a script to this header.

            :param script:  The script as script node.

                note::  Author(s): Mitch """

        self.scripts += (script,)
        self.innerHTML += (script,)
