#############################################################################
#
#
#   bfassist.network Module to BFA c7
#
#
#############################################################################
""" This module handles networking from bfa 'client' to bfa 'master' and vice-versa. The more universal parts of this
package are the 'baseclient' and 'baserequesthandler' as well as the update-thread in the master and client sub-package
respectively and lastly the 'threadedtcpserver' in the master sub-package.

If the master or client package are loaded at the start is defined by the config that gets read when importing this
module. The config is contained in the file 'config.ini' within the package folder and should follow the basic '.ini'
format. Setting groups are indicated with edgy braces '[]' and settings are defined using an equal sign.
Comments can be made using ';' or '#' chars at the start of the line. Every config needs to contain the
'BFA Settings' group containing at least the following example settings:

    [BFA Settings]
    hostname = "127.0.0.1"
    certificate = ""
    client = False
    stage = "development"
    branch = "c7"
    revision = ""
    auto-update = False
    auto-upgrade = False
    league-extensions = False


The server provided on the master-side utilises multi-threading and SSL encryption from python base modules. The master
never initiates connections but functions as a pure server. The client and request handler modules offer some basic
functionality for that. Connection/disconnecting, sending/receiving strings, json or files as well as exchange and
comparison of unique file-/folder-signatures using the sha256 from hashlib. The specific function for generating the sha
of a file can be found in the references package.

At connection start the client transfers its network config to the server. Sadly the way the interaction with the config
is done currently is very clunky and a bit ugly. Technically this deserves an own module and should be noted as a
todo:: for the not so far future.

For the sake of easy modularisation of the request handler/client a bit of import trickery was used for building them
for bfa. The init of the client and master start by importing the base versions and then apply patches by successively
importing whichever other modules are found. This means if one would want to add/remove certain request handler and/or
client methods they would merely need to fit in their own patch.

The point of implementing this was that some bf server owners might be interested in using the features of bfa but don't
want to be involved with the bf-league. These server owners don't need to download the 'leagueclient' module of the
request handler. The network package as a whole will still work regardless of if the 'leagueclient' module is available
or not.

    Dependencies:

        network ------> updatethread
            |       \-> client  (if configured as client) @startup
            |        -> master  (if configured as master) @startup
            \-> standalone      (if configured as client) @startup
             -> master          (if configured as client) @startup

        note::  Author(s): Mitch last-check: 07.07.2021 """

from os.path import exists

from bfassist.network.updatethread import UpdateThread


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


CONFIG = {}
BFA_Settings = "BFA Settings"


def getSettings(settingTuples: set):
    """ Simple function to check a set of settings specified in tuples.

        :param settingTuples:   A set containing setting tuples.

            note::  Author(s): Mitch """

    for setting in settingTuples:
        getSetting(*setting)


allowed_values = {
        bool:       {'true', 'false', '0', '1'},
}

return_values = {
    bool: {
        'true':     True,
        '1':        True,
        'false':    False,
        '0':        False
    }
}


# noinspection PyTypeChecker
def getSetting(value_type: type, key: str, group: str = None):
    """ Function to check if a setting is within the allowed target range. Otherwise raises a ValueError.
    
        :param value_type:      A set of allowed values for the setting.
        :param key:             The name or key of the setting.
        :param group:           The group this setting belongs to.
        
            note::  Author(s): Mitch """

    if group is None:
        if value_type is str:
            CONFIG[key] = CONFIG[key][1:-1]
        elif key not in CONFIG or CONFIG[key] not in allowed_values[value_type]:
            raise ValueError(key + " setting is not correctly set!")
        if value_type in return_values:
            CONFIG[key] = return_values[value_type][CONFIG[key]]
    else:
        if value_type is str:
            CONFIG[group][key] = CONFIG[group][key][1:-1]
        elif key not in CONFIG[group] or CONFIG[group][key] not in allowed_values[value_type]:
            raise ValueError(group + " " + key + " setting is not correctly set!")
        if value_type in return_values:
            CONFIG[group][key] = return_values[value_type][CONFIG[group][key]]


def readInit():
    """ Function that reads the initialisation config and sets the respective init values.

            note::  Author(s): Mitch """

    # noinspection PyShadowingNames
    with open('bfassist/network/config.ini', 'r') as configFile:
        for line in configFile:
            if line.startswith(';') or line.startswith('#'):
                pass
            elif line.startswith('[') and line.endswith(']\n'):
                CONFIG[line[1:-2]] = {}
            elif '=' in line:
                key, value = line[:line.index('=')].strip().lower(), line[line.index('=') + 1:].strip().lower()
                if isinstance(CONFIG[list(CONFIG.keys())[-1]], dict):
                    CONFIG[list(CONFIG.keys())[-1]][key] = value
                else:
                    CONFIG[key] = value
            elif line.strip() == '\n':
                pass
            else:
                raise SyntaxError("Config file does not follow the required format. Compare at: " + line)

    if "BFA Settings" not in CONFIG:
        raise ValueError("Config file does not contain the BFA Settings group." + str(CONFIG))
    else:
        getSettings({
            (str,       'hostname', BFA_Settings),
            (str,       'certificate', BFA_Settings),
            (bool,      'client', BFA_Settings),
            (str,       'stage', BFA_Settings),
            (str,       'branch', BFA_Settings),
            (str,       'revision', BFA_Settings),
            (bool,      'auto-update', BFA_Settings),
            (bool,      'auto-upgrade', BFA_Settings),
            (bool,      'league-extensions', BFA_Settings)
        })


def startup():
    """ Function that runs after making sure a config exists. It will check that the required base configuration is
    specified and then load the respectively required files.

        note::  Author(s): Mitch """

    readInit()
    if CONFIG[BFA_Settings]['client']:
        from bfassist.network import client

        if __name__ == "__main__":
            client.main()
        elif CONFIG[BFA_Settings]['auto-upgrade']:
            from bfassist.standalone import KERN

            if not KERN.AUTO_UPDATE_THREAD.active:
                KERN.AUTO_UPDATE_THREAD.start()
            if not KERN.AUTO_UPDATE_THREAD.auto_upgrading:
                KERN.AUTO_UPDATE_THREAD.auto_upgrading = True
            KERN.run()
        elif CONFIG[BFA_Settings]['auto-update']:
            from bfassist.standalone import KERN

            if not KERN.AUTO_UPDATE_THREAD.active:
                KERN.AUTO_UPDATE_THREAD.start()
            if KERN.AUTO_UPDATE_THREAD.auto_upgrading:
                KERN.AUTO_UPDATE_THREAD.auto_upgrading = False
            KERN.run()
        else:
            from bfassist.standalone import KERN

            if KERN.AUTO_UPDATE_THREAD.active:
                KERN.AUTO_UPDATE_THREAD.stop()
            if KERN.AUTO_UPDATE_THREAD.auto_upgrading:
                KERN.AUTO_UPDATE_THREAD.auto_upgrading = False
    else:
        from bfassist.network import master

        if CONFIG[BFA_Settings]['auto-upgrade']:
            from bfassist.master import MVC

            if not MVC.AUTO_UPDATE_THREAD.active:
                MVC.AUTO_UPDATE_THREAD.start()
            if not MVC.AUTO_UPDATE_THREAD.auto_upgrading:
                MVC.AUTO_UPDATE_THREAD.auto_upgrading = True
        elif CONFIG[BFA_Settings]['auto-update']:
            from bfassist.master import MVC

            if not MVC.AUTO_UPDATE_THREAD.active:
                MVC.AUTO_UPDATE_THREAD.start()
            if MVC.AUTO_UPDATE_THREAD.auto_upgrading:
                MVC.AUTO_UPDATE_THREAD.auto_upgrading = False
        else:
            from bfassist.master import MVC

            if MVC.AUTO_UPDATE_THREAD.active:
                MVC.AUTO_UPDATE_THREAD.stop()
            if MVC.AUTO_UPDATE_THREAD.auto_upgrading:
                MVC.AUTO_UPDATE_THREAD.auto_upgrading = False


def toggleAutoUpdate():
    """ Toggles the boolean value of the auto-update setting in the config dictionary as well as in the actual config
    file and finally returns the new value.

        :return:    The new boolean value.

            note::  Author(s): Mitch """

    newValue = not CONFIG[BFA_Settings]['auto-update']
    # noinspection PyUnusedLocal,PyShadowingNames
    with open('bfassist/network/config.ini', 'r+') as configFile:
        output = ""
        for line in configFile:
            if 'auto-update =' in line:
                output += 'auto-update = ' + str(newValue) + "\n"
            else:
                output += line
        configFile.seek(0)
        configFile.write(output)
        configFile.truncate()
    return newValue


def toggleAutoUpgrade():
    """ Toggles the boolean value of the auto-update setting in the config dictionary as well as in the actual config
    file and finally returns the new value.

        :return:    The new boolean value.

            note::  Author(s): Mitch """

    newValue = not CONFIG[BFA_Settings]['auto-upgrade']
    # noinspection PyShadowingNames
    with open('bfassist/network/config.ini', 'r+') as configFile:
        output = ""
        for line in configFile:
            if 'auto-upgrade =' in line:
                output += 'auto-upgrade = ' + str(newValue) + "\n"
            else:
                output += line
        configFile.seek(0)
        configFile.write(output)
        configFile.truncate()
    return newValue


if not exists('bfassist/network/config.ini'):
    print("No config found, creating a standard config.")
    try:
        with open('bfassist/network/config.ini', 'w') as configFile:
            configFile.write(
                """
                [BFA Settings]\n
                hostname = "localhost"\n
                certificate = ""\n
                client = True\n
                version = "development/c7/"\n
                stage = "development/"\n
                branch = "c7/"\n
                revision = ""\n
                auto-update = True\n
                auto-upgrade = False\n
                league-extensions = False\n
                """
            )
        client_choice = ""

        while client_choice not in {'y', 'n'}:
            client_choice = input("Do you want to run with the standard config?(y/n)")
            if client_choice == 'y':
                startup()
    except FileNotFoundError:
        print("Using module outside of valid bfa environment. Commencing without setting up the bfa network.")
else:
    if __name__ == '__main__':
        startup()
