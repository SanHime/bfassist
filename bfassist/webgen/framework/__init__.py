#############################################################################
#
#
#   webGenFramework module to BFA c7
#
#
#############################################################################
""" This is a simple HTML/JS/CSS generator/framework for the purpose of maintaining the webclient of bfa. Makes the
three 'base-document-types' stylesheet, script, html-document available.

    Dependencies:

        framework ----> css
                    \-> html
                     -> js

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webgen.framework.css import CSS_Stylesheet
from bfassist.webgen.framework.html import HTML_Document
from bfassist.webgen.framework.js import JS_Script


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass
