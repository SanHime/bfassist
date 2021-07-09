#############################################################################
#
#
#   webGen framework html miscellaneous module to BFA v.5 standalone
#
#
#############################################################################
""" Module to improve python to HTML coding with the bfa webGen modules.

    Dependencies:

        html <- tags
         |
         \-> body
          -> node

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.webgen.framework.html.body import HTML_Body
from bfassist.webgen.framework.html.node import HTML_Node, HTML_Node_Contentless


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def a(innerHTML=None): return HTML_Node('a', innerHTML=innerHTML) if innerHTML else HTML_Node('a')


def body(): return HTML_Body()


def br(): return HTML_Node_Contentless('br')


def button(): return HTML_Node('button')


def div(): return HTML_Node('div')


def fieldset(): return HTML_Node('fieldset')


def form(): return HTML_Node('form', {'accept-charset': 'utf-8'})


def h1(innerHTML=None): return HTML_Node('h1', innerHTML=innerHTML) if innerHTML else HTML_Node('h1')


def h2(innerHTML=None): return HTML_Node('h2', innerHTML=innerHTML) if innerHTML else HTML_Node('h2')


def h3(innerHTML=None): return HTML_Node('h3', innerHTML=innerHTML) if innerHTML else HTML_Node('h3')


def h4(innerHTML=None): return HTML_Node('h4', innerHTML=innerHTML) if innerHTML else HTML_Node('h4')


def Input(): return HTML_Node_Contentless('input')


def label(): return HTML_Node('label')


def option(innerHTML=None): return HTML_Node('option', innerHTML=innerHTML) if innerHTML else HTML_Node('option')


def select(): return HTML_Node('select')


def table(): return HTML_Node('table')


def tbody(): return HTML_Node('tbody')


def textarea(): return HTML_Node('textarea')


def td(innerHTML=None): return HTML_Node('td', innerHTML=innerHTML) if innerHTML else HTML_Node('td')


def th(innerHTML=None): return HTML_Node('th', innerHTML=innerHTML) if innerHTML else HTML_Node('th')


def thead(): return HTML_Node('thead')


def tr(): return HTML_Node('tr')
