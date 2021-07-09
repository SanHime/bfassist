#############################################################################
#
#
#   Network Master Module to BFA c7
#
#
#############################################################################
""" This module handles networking from bfa 'master' to bfa 'client'. In particular it builds the request handler that
is used by the master server to handle requests incoming from the clients. Again, import trickery is used to allow
simple modularisation of the request handler. Although it was not necessary to do this for the server-side it seemed
logical to do this analogue to the client.

    Dependencies:
        master -\-> baserequesthandler
                 -> leaguerequesthandler

        note::  Author(s): Mitch last-check: 07.07.2021 """

from importlib import import_module
from os import listdir

from bfassist.network.master.baserequesthandler import ThreadedTCPBaseRequestHandler
from bfassist.network.master.threadedtcpserver import BFA_ThreadedMasterTCPServer


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


ThreadedTCPRequestHandler = ThreadedTCPBaseRequestHandler

try:
    for file in listdir('bfassist/network/master/'):
        if file.endswith('.py') and not (file.startswith('__init__') or file.startswith('baserequesthandler')):
            import_module('bfassist.network.master.' + file[:-3])
except FileNotFoundError:
    print("Using module outside of valid bfa environment. Commencing without setting up bfa network for bfa master.")
