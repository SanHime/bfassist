#############################################################################
#
#
# Module of BFA that provides some utilities for dealing with the Remote Console
#
#
#############################################################################
""" This module is supposed to provide some necessary and useful utilities for interacting with the BF Remote Console.

    Dependencies:

        bfassist <- (standalone.server.)bfcutil
            \
             -> bfa_logging

        todo::  Rework?!
        note::  Author(s): Mitch, henk last-check: 08.07.2021 """

from struct import pack

from bfassist.bfa_logging import log


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def buildHenkCommand(commandType: str, args: list):
    """ This function builds specific bytes to send as custom command to a server with a binary modified by henk.

        :param commandType: Type of henk command to build.
        :param args:        List of arguments to be used for building the command.

        :return:        The henk command.

            note::  Author(s): Mitch, henk """

    kargs = args.copy()
    global henkscommands
    log('Building a henk command.', 0)
    if commandType in henkscommands:
        log('Executing a henk command.', 1)
        return henkscommands[commandType](kargs)
    else:
        return False


def buildTpTo(args: list):
    """ This function builds specific bytes to send as custom teleportation command
    to a server with a binary modified by henk.

        :param args:    List of arguments used for building the command.
                        In particular the player id and coordinates to tp to

        :return:        A teleportation command based on henk's command standard.

            note::  Author(s): Mitch, henk """

    global henkscommands

    henkcommand = ''
    henkcommand += bytes.fromhex('566172732e6765742063757374').decode('ISO-8859-1')  # cust - henkcommand flag
    henkcommand += bytes.fromhex('50').decode('ISO-8859-1')  # tp - type of henkcommand

    idarray = str(pack('i', (int(args[0]))).hex())

    henkcommand += bytes.fromhex('f'+idarray[1]+idarray[0]+'f').decode('ISO-8859-1')

    # Added player id

    coordinates = args[1].split('/')
    for x in range(3):
        henkcommand += varToCustVar(coordinates[x], 'f')
    # Added coordinates

    henkcommand += bytes.fromhex('0a').decode('ISO-8859-1')  # end of henkcommand

    return henkcommand


def buildSetPlayerToTeam(args: list):
    """ This function builds specific bytes to send as custom set player to team command to a server with a binary
    modified by henk.

        :param args:    List of arguments used for building the command.
                        In particular the id of the player and team to set it to.

        :return:        A set player to team command based on henk's command standard.

            note::  Author(s): henk, Mitch """

    henkcommand = ''
    henkcommand += bytes.fromhex('566172732e6765742063757374').decode('ISO-8859-1')  # cust - henkcommand flag
    henkcommand += bytes.fromhex('54').decode('ISO-8859-1')  # tp - type of henkcommand

    idarray = str(pack('i', int(args[0])).hex())

    henkcommand += bytes.fromhex('f' + idarray[1] + idarray[0] + 'f').decode('ISO-8859-1')

    henkcommand += varToCustVar(int(args[1]), 'i')

    return henkcommand


def varToCustVar(value, inType: str):
    """ ...

        :param value:   ...
        :param inType:  ...

        :return:        ...

            note::  Author(s): henk, Mitch """

    inVar = str(pack(inType, value).hex())  # e.g. 00 00 7a 44
    inarray = [inVar[:2], inVar[2:4], inVar[4:6], inVar[6:8]]
    inarray = inarray[::-1]

    rdword = [inarray[0][0]+'f', 'f'+inarray[1][1], inarray[2][0]+'f', 'f'+inarray[3][1]]

    ldword = ['f'+inarray[0][1], inarray[1][0]+'f', 'f'+inarray[2][1], inarray[3][0]+'f']

    custVar = bytes.fromhex("".join(ldword[::-1]) + "".join(rdword[::-1]))

    return custVar.decode('ISO-8859-1')


henkscommands = {
    'tpTo':    buildTpTo,
    'setPlayerToTeam':  buildSetPlayerToTeam
}
