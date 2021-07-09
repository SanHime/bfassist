#############################################################################
#
#
#   Webclient Headings Module to BFA c7 Standalone
#
#
#############################################################################
""" This module makes headings/heading-styles used in the webclient available.

    Dependencies:

        bfassist <- (standalone.)webclient <- headings
            |                       \
            \                        -> colourscheme
             -> framework --\-> html
                             -> css

        note::  Author(s): last-check: 08.07.2021 """

from bfassist.standalone.webclient.colourscheme import BFA_COLOURS
from bfassist.webgen.framework.html import *
from bfassist.webgen.framework.css import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


BFA_GREEN_CENTERED_H1 = h1().styleThisType({set_text_align('center'), set_colour(BFA_COLOURS.GREEN)})


def createH1(heading: str):
    """ Simple function that creates and returns the standard heading used for the offline view.

        :param heading: The text of the heading.

        :return:        HTML containing the standard heading.

            note::  Author(s): Mitch """

    Heading = h1()
    Heading.Id = "heading"
    Heading.innerHTML = heading
    return Heading, BFA_GREEN_CENTERED_H1
