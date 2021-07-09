#############################################################################
#
#
# Module of BFA introducing and managing the Server Map Interface Class
#
#
#############################################################################
""" This module manages the interface and interactions of the server objects with the references map module.

    Dependencies:

        bfassist <- (standalone.)server <- interfacemap
            |
            \-> references
             -> bfa_logging

        note::  Author(s): Mitch last-check: 08.07.2021 """

from os import listdir
from os.path import isdir
from shutil import copyfile

from bfassist.standalone.server import Server
from bfassist.references import Map, Maps, shaForFile, getDir, createSafeReference
from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


from_mod_to_levels = "/archives/bf1942/levels"


class ServerMapInterface:
    """ The server map interface lets a server object interact with its map files.

        :param server:      The server this interface belongs to.
        :param pathToMods:  The path to the mods directory for better readability.

            note::  Author(s): Mitch """

    def __init__(self, server: Server, pathToMods: str = None):

        self.server = server

        if pathToMods:
            self.pathToMods = pathToMods
        else:
            self.pathToMods = self.server.getBFPath() + "mods/"

    def isAMod(self, inMod: str):
        """ Simple function to check if a mod exists and has the required levels folder in which maps would be.

            :param inMod:   The name of the mod directory we're trying to check.

            :return:        True if the mod directory exists and the corresponding levels folder to.

                note::  Author(s): Mitch """

        if isdir(self.pathToMods + inMod) and isdir(self.pathToMods + inMod + from_mod_to_levels):
            return True
        else:
            return False

    def overwriteMapWithStandardVersion(self, fullMapName: str, mapReference: Map = None):
        """ Function that overwrites a map in the server with its standard version. This should be only called if the
        current version has been backed up already.

            :param fullMapName:     The fully qualified map name i.e. the path starting from the mods folder.
            :param mapReference:    The map object of the standard version.

                note::  Author(s): Mitch """

        if mapReference is None:
            mapReference = Maps[fullMapName]
        copyfile(mapReference.getPath() + mapReference.getName(), self.pathToMods + fullMapName)
        mapReference.addPath(self.pathToMods + getDir(fullMapName))

    def backupAnInstalledMapAndFreeItsReference(self, mapReference: Map):
        """ Function to back up a map that's currently installed (and has a reference!!!) freeing its spot for
        replacement by setting its original Digest to a null string.

            :param mapReference:    The corresponding map object.

                note::  Author(s): Mitch """

        mapReference.setDigest("")
        if Maps.fetchSingleWhere('Digest', shaForFile(mapReference.getPath() + mapReference.getName())):
            log("This exact version of " + mapReference.getName() + " has been backed up before. Abandoning backup.", 2)
            return
        else:
            safeReference = createSafeReference(self.pathToMods + mapReference.getFName(), 'maps/' +
                                                mapReference.getFName())
            Map.fromReference(safeReference)

    def refreshAnAlreadyReferencedMap(self, fullMapName: str):
        """ Function that refreshes a map that has already been referenced previously.

            :param fullMapName: The fully qualified map name i.e. the path starting from the mods folder.

                note::  Author(s): Mitch """

        mapReference = Maps[fullMapName]
        if mapReference.getDigest() == shaForFile(self.pathToMods + fullMapName):
            if self.pathToMods + fullMapName not in mapReference.getPaths():
                mapReference.addPath(self.pathToMods + getDir(fullMapName))

        else:
            safeReference = createSafeReference(self.pathToMods + fullMapName, 'maps/' + fullMapName)  # backup version
            Map.fromReference(safeReference)  # make a db entry for the backup
            self.overwriteMapWithStandardVersion(fullMapName, mapReference)  # overwrite with standard version

    def refreshMaps(self):
        """ Function to refresh our knowledge about the installed maps.

                note::  Author(s): Mitch """

        log("Refreshing maps this may take a while.", 2)
        if not isdir(self.pathToMods):
            log("Path to mods is invalid. Could not refresh maps!", 3)
        else:
            for mod in listdir(self.pathToMods):
                if self.isAMod(mod):
                    for modMap in listdir(self.pathToMods + mod + from_mod_to_levels):

                        fullMapName = mod + from_mod_to_levels + modMap

                        if fullMapName not in Maps:
                            Map.fromReference(self.pathToMods + fullMapName)
                        else:
                            self.refreshAnAlreadyReferencedMap(fullMapName)
            log("Finished refreshing maps.", 2)

    def addMapFromReference(self, mapReference: Map):
        """ Function to install a map from a reference map object. If it's been installed before it will merely
         overwrite itself.

            :param mapReference:    Map object to be installed.

                note::  Author(s): Mitch """

        # todo:: self.writeToServer("Installing the map file " + mapReference.getName() + "...")
        copyfile(mapReference.getPath() + mapReference.getName(), self.pathToMods + mapReference.getFName())
        mapReference.addPath(self.pathToMods + getDir(mapReference.getFName()))
        # todo:: self.writeToServer("Successfully installed " + mapReference.getName())

    def replaceMapReferenceWithMapFromReference(self, mapReference: Map, referencePath: str):
        """ Function to replace a current version of a map with a new one from a reference. For that we'll backup the
        current version and then put the new one in all places that were occupied by the current version.

            :param mapReference:    The map object of the current version.
            :param referencePath:   The path to the new reference version.

                note::  Author(s): Mitch """

        self.backupMap(mapReference)
        mapReference.setDigest(shaForFile(referencePath))
        for location in mapReference.getPaths():
            copyfile(referencePath, location + mapReference.getName())

    def replaceMapWithVariation(self, mapReference: Map, variationReference: Map):
        """ Function to replace a current version of a map with an already existing variation. For that we'll simply
        create a backup for the current version and then replace it with the variation and delete the variation backup.

            :param mapReference:        Original map to be backed up and replaced.
            :param variationReference:  Variation of the map to be installed.

                note::  Author(s): Mitch """

        # Confirm that the variation is truly a variation of the map to be replaced
        if mapReference.getFName() == variationReference.getFName():
            self.backupMap(mapReference)
            for location in mapReference.getPaths():
                copyfile(variationReference.getPath() + variationReference.getName(), location + mapReference.getName())

            digestOfVariation = variationReference.getDigest()
            variationReference.delete()
            mapReference.setDigest(digestOfVariation)
