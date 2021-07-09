#############################################################################
#
#
# Server Map Module that manages maps for the servers
#
#
#############################################################################
""" This module offers all sorts of functions required for the interaction and distribution of and with bf maps using
the sql package for archiving.

    Dependencies:

        bfassist <- (references.)maps
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


if not exists('bfassist/references/maps'):
    try:
        mkdir('bfassist/references/maps')
    except FileNotFoundError:
        print("Using module outside of valid bfa environment. Commencing without setting up bf maps.")


class Map(DBStorable, table="servermaps", live=True):
    """ A class to represent a reference to a bf map available on the server with at least one specific location.

        :param FName:       Fully qualified name of this name. (Including mod)
        :param Digest:      The 256-SHA hex-digest of this map file.
        :param Name:        The name of this map.
        :param Paths:       A set of locations of this map.

            note::  Author(s): Mitch """

    def __init__(self, FName: str, Digest: str, Name: str, Paths: set):
        self.SFName = FName, TINYTEXT, PRIMARY_KEY
        self.SDigest = Digest, TEXT, UNIQUE
        self.SName = Name, VARCHAR(255)
        self.SPaths = Paths, TINYTEXT

        self.insertToDB()

    @classmethod
    def fromReference(cls, path: str):
        """ Simplified constructor just using a file reference.

            :param path:        Location of the file.

                note::  Author(s): Mitch """

        from bfassist.references import shaForFile

        if exists(path):
            cls(path[path[:path.rfind('/') - len("/archives/bf1942/levels")].rfind('/') + 1:], shaForFile(path),
                path.split('/')[-1], {path[:path.rfind('/') + 1]})

    def addPath(self, inPath: str):
        """ Simple function to add an additional location.

            :param inPath:  The location to add.

                note::  Author(s): Mitch """
        paths = self.getPaths()
        paths.add(inPath)
        self.setPaths(paths)

    def getPath(self):
        """ Simple function to retrieve just a single path.

            :return:    Path to a location of this map.

                note::  Author(s): Mitch """

        return next(iter(self.getPaths()))


Maps = Map.storageDict
