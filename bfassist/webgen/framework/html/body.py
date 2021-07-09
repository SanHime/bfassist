#############################################################################
#
#
#   HTML Body webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a HTML body module for a simple HTML/JS/CSS generator/framework with the purpose of maintaining the
webclient of bfa.

    Dependencies:

        body
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


class HTML_Body(HTML_Node):
    """ Representation of the HTML body.

            note::  Author(s): Mitch """

    def __init__(self, nodeType: str = 'body'):

        super().__init__(nodeType)
