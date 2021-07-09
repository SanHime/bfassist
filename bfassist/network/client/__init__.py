#############################################################################
#
#
#   network Client Module to BFA c7
#
#
#############################################################################
""" This module handles networking from bfa 'client' to bfa 'master'. In particular it builds the BFA_CLIENT that's
used to communicate with the master. Some import trickery is used to allow simple insertion of additional methods to the
client. The leagueclient is an example for that. If wanting to make your own module-extension just import the
BFA_CLIENT variable, let your class-extension inherit from it and overwrite BFA_CLIENT with your extension in the end.

    Dependencies:

        client -\-> baseclient
                 -> leagueclient (if available)

        note::  Author(s): Mitch last-check: 07.07.2021 """

from importlib import import_module
from os import listdir

from bfassist.network.client.baseclient import BFABaseClient


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


BFA_MASTER_IP = '49.12.106.25'
BFA_MASTER_PORT = 1943

BFA_CLIENT = BFABaseClient()


try:
    for file in listdir('bfassist/network/client/'):
        if file.endswith('.py') and not (file.startswith('__init__') or file.startswith('baseclient')):
            import_module('bfassist.network.client.' + file[:-3])
except FileNotFoundError:
    print("Using module outside of valid bfa environment. Commencing without setting up bfa network for bfa client.")
