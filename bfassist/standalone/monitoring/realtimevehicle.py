#############################################################################
#
#
# Module of BFA that manages server statistics in realtime
#
#
#############################################################################
""" This module implements the real-time logging of in-game statistics specifically that of bf vehicles/PCOs.

    Dependencies:

        2nd-party dependency numpy

        note::  Author(s): Mitch last-check: 08.07.2021 """

from numpy import array


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class RealTimeVehicle:
    """ A vehicle that's spawned on a server can have a corresponding real time vehicle object to track it.

        :param Id:              Refractor id of the vehicle.
        :param position:        Position of the vehicle as numpy array.
        :param rotation:        Rotation of the vehicle as numpy array.
        :param velocity:        Velocity of the vehicle.
        :param acceleration:    Acceleration of the vehicle.
        :param is_fake:         1 if fake vehicle otherwise 0.
        :param seats:           A dictionary containing seat ids as keys and real time players as values if the seat
                                with id is occupied by real time player.

            note::  Author(s): Mitch, henk """

    def __init__(self, Id: int = None, position: array = None, rotation: array = None, velocity: float = None,
                 acceleration: float = None, is_fake: int = None, seats: dict = None):
        self.Id = Id
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.acceleration = acceleration
        self.is_fake = is_fake
        if seats:
            self.seats = seats
        else:
            self.seats = {}

    @staticmethod
    def typeHint():
        return {
            'Id': int,
            'position': str,
            'rotation': str,
            'velocity': float,
            'acceleration': float,
            'is_fake': int
        }

    def toLocalDict(self):
        """ Function for getting the real time vehicle object as a dictionary of strings representing attributes and the
        values for the local bfa perspective so it can also be json serialised. (without seats)

            :return:    Real time vehicle as a dictionary.

                note::  Author(s): Mitch """

        return {
            'Id':           self.Id,
            'position':     "".join(array2string(self.position, separator='/')[1:-1].split()),
            'rotation':     "".join(array2string(self.rotation, separator='/')[1:-1].split()),
            'velocity':     self.velocity,
            'acceleration': self.acceleration,
            'is_fake':      self.is_fake
        }
