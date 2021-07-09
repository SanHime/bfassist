#############################################################################
#
#
#   Refractor Module to BFA c7 Standalone
#
#
#############################################################################
""" This module will contain references mainly to files that are relevant to bfa. Contains a few miscellaneous functions
like calculating a sha for a file and similar stuff. Also used to archive files utilising the sql package.

    Dependencies:

        references \-> binaries
                    -> maps

        note::  Author(s): Mitch last-check: 07.07.2021 """

from os import mkdir, listdir
from os.path import isdir
from shutil import copyfile
from hashlib import sha256

from bfassist.references.binaries import Binary, Binaries
from bfassist.references.maps import Map, Maps


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def shaForFile(inPath: str):
    """ Function that calculates and returns the sha-256 hex-digest hash for a file given it's path.

        :param inPath:  Path to the file.

        :return:        SHA-256 hash hex-digest.

            note::  Author(s): Mitch """

    with open(inPath, "rb") as f:
        sha = sha256()
        for block in iter(lambda: f.read(4096), b""):
            sha.update(block)

    return sha.hexdigest()


def createDirectoryStructure(structure: str):
    """ Function that sequentially creates a directory structure specified by a string.

        :param structure:   A string that defines a sequential structure of (sub-)directories.

            note::  Author(s): Mitch """

    subDirectories = structure.split('/')[:-1]
    currentDirectory = "bfassist/references/"

    for subDirectory in subDirectories:
        if not isdir(currentDirectory + subDirectory):
            mkdir(currentDirectory + subDirectory)
        currentDirectory = "bfassist/references/" + subDirectory + "/"


def createSafeReference(originFile: str, fullReferencePath: str = ""):
    """ Function that creates a reference/backup of a file "safely" meaning, that if a reference like this already
    exists. It will create a new one by appending a suffix. Returns the path to the thereby created reference.

        :param originFile:          The file to create a reference for.
        :param fullReferencePath:   Supplementary specification of the path if it should not be referenced directly from
                                    the references directory.

        :return:                    The path to the reference.

            note::  Author(s): Mitch """

    if not isdir('bfassist/references/' + getDir(fullReferencePath)):
        createDirectoryStructure(fullReferencePath)

    variationCount = 0
    variationSuffix = ""
    while exists('bfassist/references/' + fullReferencePath + variationSuffix):
        variationSuffix = "variation" + str(variationCount)
        variationCount += 1

    copyfile(originFile, 'bfassist/references/' + fullReferencePath + variationSuffix)

    return 'bfassist/references/' + fullReferencePath + variationSuffix


def getDir(originFile: str):
    """ Simple function that returns the directory a file is in. Essentially just cuts the filename from the input.

        :param originFile:  Path to a file.

        :return:            Path to the directory of the file including the dir-indicating slash at the end.

            note::  Author(s): Mitch """

    return originFile[:originFile.rfind('/') + 1]


def listFMapNames(inDir: str):
    """ Function that examines a directory for fully qualified map names and returns a list of them.

        :param inDir:   The directory to look for the maps in.

        :return:        List of fully qualified map names found.

            note::  Author(s): Mitch """

    fMapNames = []
    mods = listdir(inDir)
    for mod in mods:
        if isdir(inDir + "/" + mod + "/archives") and isdir(inDir + "/" + mod + "/archives/bf1942") and\
           isdir(inDir + "/" + mod + "/archives/bf1942/levels"):
            for inMap in listdir(inDir + "/" + mod + "/archives/bf1942/levels"):
                fMapNames.append(mod + "/archives/bf1942/levels/" + inMap)
    return fMapNames
