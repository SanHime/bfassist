#############################################################################
#
#
#   Core Module to BFA c7 Master
#
#
#############################################################################
""" This is the Core Module of the BFA master server. It can be imported into a python3.7+ cli-session and operated
using the functions made available in its sub modules.

At import you will be prompted to choose whether you want to run the master server on the development or on the
experimental stage since that's the only two opened stages thus far.

The two important variables here are 'master' which is a custom multi-threaded master tcp server based on python base
modules and 'MVC' which is a simple version control system to make the master aware of which "version" is available and
running.

For now the intention is to run three master servers, one for each stage, where they are the only central master server
respectively. However, a distributed version could also be feasible in the future.

This setup is very much tailored towards what I envision for the future of bfa, however with some customisation it can
probably be recycled and applied for other similar projects that use a master-server like instance.

    Dependencies:

        bfassist <- master -> bfaversioncontrol
            \
             -> network -> master


        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.master.bfaversioncontrol import MasterVersionControl
from bfassist.network import *
from bfassist.network.master import BFA_ThreadedMasterTCPServer


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


HOST = CONFIG[BFA_Settings]['hostname']
CERT = CONFIG[BFA_Settings]['certificate']

SVN_BASE_URL = "http://49.12.106.25/svn/s5/"
SVN_USERNAME = "bfleague"
SVN_PASSWORD = "gamespy"

DEVELOPMENT_STAGE = "development/"
EXPERIMENTAL_STAGE = "experimental/"

DEVELOPMENT_ACTIVE_BRANCH = "c7/"
DEVELOPMENT_ACTIVE_CLIENT_REVISION = "1869"

EXPERIMENTAL_ACTIVE_BRANCH = "c7/"
EXPERIMENTAL_ACTIVE_CLIENT_REVISION = None

DEVELOPMENT_STAGE_PORT = 1943
EXPERIMENTAL_STAGE_PORT = 1942
# When the stable stage will be opened it will increment the other port numbers by one and itself occupy the 1942 port

MVC = None
master = None
stage = CONFIG[BFA_Settings]['stage']

try:
    if stage in DEVELOPMENT_STAGE:
        MVC = MasterVersionControl(
            SVN_BASE_URL, DEVELOPMENT_STAGE, DEVELOPMENT_ACTIVE_BRANCH, DEVELOPMENT_ACTIVE_CLIENT_REVISION
        )
        master = BFA_ThreadedMasterTCPServer(HOST, DEVELOPMENT_STAGE_PORT, pemchain=CERT)

    elif stage in EXPERIMENTAL_STAGE:
        MVC = MasterVersionControl(
            SVN_BASE_URL, EXPERIMENTAL_STAGE, EXPERIMENTAL_ACTIVE_BRANCH, EXPERIMENTAL_ACTIVE_CLIENT_REVISION
        )
        master = BFA_ThreadedMasterTCPServer(HOST, EXPERIMENTAL_STAGE_PORT, pemchain=CERT)
    else:
        pass
except OSError:
    print("Address still in use. Try again ...")


def main():
    global master

    master.startup()
