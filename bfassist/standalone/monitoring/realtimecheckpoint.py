#############################################################################
#
#
# Module of BFA that manages server statistics in realtime
#
#
#############################################################################
""" This module implements the real-time logging of in-game statistics specifically for one current bf checkpoint.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 08.07.2021 """


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class RealTimeCP:
    """  A control point that exists on a map can have a corresponding real time control point to track it.

        :param Id:      Refractor id of this control point.
        :param team:    Team the control point is currently controlled by.

            note::  Author(s): Mitch, henk """

    def __init__(self, Id: int = None, team: int = None):
        self.Id = Id
        self.team = team
