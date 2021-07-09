#############################################################################
#
#
#   BFA User System - BFA User Module to BFA c7
#
#
#############################################################################
""" This module defines the rights that bfa users can hold. The available 'rights' are specified in the BFARights list.

    Dependencies:

        None

        note::  Author(s): Mitch last-check: 07.07.2021 """

from __future__ import annotations


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


class BFARight:
    """ A class that's supposed to simplify the interaction with rights and permissions of bfa users.

        :param Name:    The name and identifier of a right.

            note::  Author(s): Mitch """

    BFARights = ['Rightless', 'Default', 'Admin', 'SuperAdmin']

    def __init__(self, Name: str):
        if Name in self.BFARights:
            self.Name = Name
        else:
            raise ValueError(Name + " is not an allowed right. Allowed rights: " + self.BFARights)

    @staticmethod
    def typeCheck(other):
        if isinstance(other, BFARight):
            return True
        else:
            raise ValueError(other + " is not a right.")

    def __eq__(self, other):
        if self.typeCheck(other):
            if self.Name == other.Name:
                return True
            else:
                return False

    def __gt__(self, other: BFARight):
        if self.typeCheck(other):
            if self.BFARights.index(self.Name) > self.BFARights.index(other.Name):
                return True
            else:
                return False

    def __lt__(self, other):
        if self.typeCheck(other):
            if self.BFARights.index(self.Name) < self.BFARights.index(other.Name):
                return True
            else:
                return False

    def __ge__(self, other):
        if self.typeCheck(other):
            if self.__gt__(other) or self.__eq__(other):
                return True
            else:
                return False

    def __le__(self, other):
        if self.typeCheck(other):
            if self.__lt__(other) or self.__eq__(other):
                return True
            else:
                return False

    @staticmethod
    def typeHintBFARights():
        return list

    @staticmethod
    def typeHint():
        return {'Name': str}

    def toLocalDict(self):
        return {'Name': self.Name}
