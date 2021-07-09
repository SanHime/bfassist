#############################################################################
#
#
# Module of BFA that manages server statistics in realtime
#
#
#############################################################################
""" This module implements the real-time logging of in-game statistics specifically that of bf events.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 08.07.2021 """


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class RealTimeEvent:
    """ Any event in the event log is supposed to be instantiated as real time event and saved in the event dictionary
    of the corresponding real time round.

        :param eventType:   Type of the event.
        :param parameters:  All parameters of this event and their values.

            note::  Author(s): Mitch """

    def __init__(self, eventType: str, parameters: dict = None):
        self.eventType = eventType
        if parameters:
            self.parameters = parameters
        else:
            self.parameters = {}
