#############################################################################
#
#
# Server Binary Module that manages maps for the servers
#
#
#############################################################################
""" This module offers all sorts of functions required for the interaction and distribution of and with the bf server
executable using the sql package for archiving.

    Dependencies:

        bfassist <- (references.)binaries
            |
            \-> sql
             -> references  @Binary.fromReference

        note::  Author(s): Mitch last-check: 07.07.2021 """

from os import mkdir
from os.path import exists

from bfassist.sql import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


if not exists('bfassist/references/binaries'):
    try:
        mkdir('bfassist/references/binaries')
    except FileNotFoundError:
        print("Using module outside of valid bfa environment. Commencing without setting up bf executables.")


class Binary(DBStorable, table="serverbinaries", live=True):
    """ A class to represent a bf server binary file for easier management of different available binaries.

        :param Name:    The name of this binary.
        :param Digest:  The 256-SHA hex-digest of this binary file.
        :param Path:    The path to this version of the binary. Unlike for maps this points ONLY to a reference and
                        never to a currently used binary.

            note::  Author(s): Mitch """

    def __init__(self, Name: str, Digest: str, Path: str):

        self.SName = Name, VARCHAR(255), PRIMARY_KEY
        self.SDigest = Digest, TEXT, UNIQUE
        self.SPath = Path, VARCHAR(255)

        self.insertToDB()

    def toGlobalDict(self):
        """ Simple function to turn a binary into a dictionary for the global bfa perspective so it can
         also be json serialised.

             :return:    Binary as a dictionary.

                 note::  Author(s): Mitch """

        return {
            'Name': self.getName(),
            'Digest': self.getDigest()
        }

    @classmethod
    def fromReference(cls, path: str):
        """ Simplified constructor just using a file reference.

            :param path:    Location of the file.

                note::  Author(s): Mitch """

        from bfassist.references import shaForFile

        if exists(path):
            cls(path.split('/')[-1], shaForFile(path), path[:path.rfind('/')+1])


Binaries = Binary.storageDict
