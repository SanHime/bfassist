#############################################################################
#
#
#   BF-Assist c7-branch
#
#
#############################################################################
""" This is the top/root module of bf-assist. A software that's supposed to assist with the administration and
maintenance of Battlefield 1942 and its game servers. As of the last check it contains the following package structure:

    c7

        bfassist -----> api
                    |-> certificates
                    |-> colours
                    |-> master ---> league
                    |-> network \-> client
                    |            -> master
                    |-> references ---> binaries    -> league
                    |               \-> eventlogs   -> import
                    |                -> maps        -> league
                    |-> sql
                    |-> standalone ---> admin
                    |               |-> api
                    |               |-> monitoring
                    |               |-> refractor
                    |               \-> server
                    |                -> webclient ----> bfaconsole
                    |                               |-> offline
                    |                               |-> setup
                    |                               \-> update
                    |                                -> webclient
                    |-> usersystem
                    |-> webgen ---> framework ----> css
                    |                           \-> html
                    |                            -> js
                    \-> webservice ---> requesthandler
                     -> bfa_logging

        setup

    Short description of the packages and their dependencies if any.

    api             The api module  can be used independently from bfa to help weaving in light-weight api capabilities
                    to any python project supporting the typing features used. Bfa is supposed to run on python 3.7 and
                    therefore can't utilise some features from the newer python typing packages that could be really
                    useful for extending functionality. The webservice and webgen packages offer some handy support
                    functions for the api package. For instance making the api available from HTTPS and generating
                    HTML, JS to interact with it.

                    No dependencies.

    certificates    Currently this package really just offers a bog-standard way for generating an SSL-certificate.
                    More functionality for administrating certificates, for instance auto-replacing expired certs
                    etc. was/is intended but probably won't be added any soon. Could potentially be replaced by some
                    already existing package that we were too lazy to search for.

                    It requires crypto from OpenSSL as 2nd party dependency.

    colours         Similar type of package as 'certificates'. Barely offers any functionality, but is useful in its own
                    regard and supports the webgen package well.

                    No dependencies.

    master          One of the main/big packages of bf-assist. Contains the main code required to run a bfa master
                    server.

                    For the future of bfa the following release-strategy is intended.
                    There should be 3 master servers representing the 3 version-stages of bfa:
                    The development, experimental and stable stage.
                    Each server will gain the ability to redirect connecting clients to the correct stage depending on
                    version information the client will send alongside requests. Version information is further
                    constituted by a branch code which is a code consisting of a single letter and digit as well as the
                    number of the last revision of the files in the SVN repository.

                    By the time of the first public bfa release only the development and experimental stage will run.

                    Since bfa is being developed closely linked with the purposes of the bf-league its content and
                    capabilities are currently mostly catering towards needs of the league. However, the contents are
                    not meant to be limited to that and league extensions for the client side of bfa are optional as
                    will be further explained for the standalone package.

                    The dependencies of the master package are as follows:

                    bfassist -----> certificates
                                |-> network -> master
                                |-> references
                                \-> sql
                                 -> bfa_logging

                    However, while the master can be loaded and does run like this, it requires to be embedded in the
                    full c7-branch bfassist structure to be able to relay the client files and support the update and
                    auto-update features of bfa.

    network         The network package is still a bit clunky after the rework for the public release but it does its
                    job and can be easily refitted to also be useful for different applications. The package handles
                    the communication 'standalone-client -> master'.

                    The client always communicates with the master via request. It sends its network config file at the
                    start and then leaves the procession of its request to the master. A request may require some back
                    and forth between the client and the master but at the end of the procession the connection will be
                    closed. All traffic is SSL encrypted with the certificate of the master.

                    The dependencies of this package are a bit complicated. If the package is configured as client it
                    will always require:

                    bfassist -----> references
                                \-> (sql - dependency of bfa_logging)
                                 -> bfa_logging

                    If it's furthermore also configured to use the league-extensions it will also require.

                    bfassist -----> standalone

                    If the package is configured as master it's generally equivalent to the master package itself and
                    therefore has the same dependencies as the master package:

                    bfassist -----> certificates
                                |-> master
                                |-> references
                                \-> sql
                                 -> bfa_logging

    references      This package is mainly used for interacting with reference files for bf servers. For instance it
                    assists in managing binary executable files and maps. Also it offers some utility for dealing with
                    bf event logs. It's an exemplary use of the sql package for managing files.

                    Only dependency is:

                    bfassist -----> sql

    sql             Useful light-weight sql integration for python. Natively utilises sqlite3 but can be easily scaled
                    to mysql or postgresql. Main functionality: SQL database as python dictionary and size-management
                    for setting a database-size threshold. The management will automatically delete data in the order of
                    priority rules specified to remain below the size-threshold.

                    No dependencies.

    standalone      Oldest and core functionality of bfa. A package to assist with the administration of bf servers run
                    on the same machine. Contains an exemplary implementation of the api and the web service. Otherwise,
                    very bf-specific. The standalone can be installed using the 'setup.py'.

                    The dependencies are as follows:

                    bfassist -----> api
                                |-> certificates
                                |-> colours
                                |-> network --> client
                                |-> references -\-> binaries
                                |                -> maps
                                |-> sql
                                |-> standalone
                                |-> usersystem
                                |-> webgen
                                \-> webservice
                                 -> bfa_logging

                    The league extensions will fit in the following places if enabled:

                    bfassist -----> network -> client ---> leagueclient
                                |-> references -\-> binaries ----> league
                                \                -> maps --------> league
                                 -> standalone --> admin ----> administrationleague

    usersystem      A very simplistic user system, tailored to the needs of bf. Used as access-restriction for the
                    webservice/api and in-game admin capabilities. Can be easily customised.

                    Dependencies:

                    bfassist ---\-> sql
                                 -> bfa_logging

    webgen          Ambitious web-generator/framework to programmatically generate "Views"(HTML, JS, CSS) that can then
                    be served via a webserver, in the case of bfa, the included webservice. Sort of follows concepts of
                    the model-view-presenter-scheme but remains only implementing what's necessary for bfa to function
                    the way it is supposed to. Flask or Django might have been a more appropriate choice but seemed like
                    an over-kill at the start of the project. Bfa will probably continue to go with webgen and grow it
                    according to its needs.

                    The webgen package is not inherently dependent on any other packages apart from colours. However,
                    certain functions in the package are so tailored to the needs of bfa that they are dependant on
                    the standalone. So the dependencies are like this:

                    bfassist ---\-> colours
                                 -> (standalone)

    webservice      A light-weight web server based on the python base HTTP server. It's ported to support only HTTPS
                    encrypted with a SSL certificate that can be automatically generated if no other certificate is
                    supplied.

                    It implements handling of GET/POST/PUT requests for the purpose of enabling a web-api in concurrence
                    with the api package. However, it's very easy to exclude the API functionality and simply run it as
                    a light-weight HTTPS web server or even remove the encryption if that's desired.

                    For serving web-sites it requires 'View' objects instantiated through the webgen module.

                    Furthermore it implements a light-weight session-management protocol that lets people identify with
                    (keyhash)/username/password from the usersystem package. By default api and web-service are hidden
                    behind a single 'offline View' and only become visible to clients that have logged in previously.
                    Session-integrity is maintained with a cookie that expires after 15 minutes on default.

                    Dependencies:

                    bfassist -----> api
                                |-> certificates
                                |-> (colours - dependency of webgen)
                                |-> (sql - dependency of usersystem)
                                |-> usersystem
                                \-> webgen
                                 -> bfa_logging

    bfa_logging     A very simplistic logging module made to be compatible with the database. Called bfa_logging to
                    prevent name conflicts with the native logging module.

                    Dependency:

                    bfassist -----> sql

    The setup module is a collection of the necessary functions to properly download and install the standalone version.

Many objects in the project have methods casting them to dictionaries that only contain json-serialisable data to ease
the transmission of data. When this method is called 'toLocalDict' it signifies that this dictionary is only
'transmitted' locally for instance via the web-api. 'toGlobalDict' signifies that this dictionary is used for
transmission between client and master/server.

Some more details about the documentation in this project. The

        "note::     Author(s):"     are supposed to specify the authors that contributed to the very file or
                                    function/method they are attached to. They do not indicate authorship of
                                    sub-modules.

        "note::     last-check:"    signifies when a module has last been reviewed with care by at least one of the
                                    authors.

Each package contains dependency-information for its subpackages, if it has any, after an initial description of the
content in terms of bfa internal dependencies or 2nd-party dependencies.
Each module contains dependency-information for itself. Like:

    Dependencies:

        bfassist --> network
            |
            |-> network     @main
            \->standalone   @main
             ->master       @main

Dependencies in the graph appear in the order they would appear at run/load-time. Imports nested into a lower namespace
are specified with an @-symbol.

The dependency information is mainly supposed to help writing and understanding the __preload__ and __postload__
function that each module needs to have in order to be able to gracefully upgrade at runtime. The dependency information
does not include dependencies resulting from the pre- and postload functions. The functions should be placed right under
the module level imports.

At upgrade time the preload function of the currently installed version will be called. Then the module will be reloaded
and the postload function will be called. Overriding these functions according to the changes made in a module will be
enough to ensure graceful updates at runtime.

        note::  Author(s): Mitch last-check: 08.07.2021 """

from bfassist.network import *


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


startup()


def main():
    from bfassist.network import CONFIG, BFA_Settings

    if CONFIG[BFA_Settings]['client']:
        import bfassist.standalone.__main__
    else:
        from bfassist.master import MVC, master, main
        main()


if __name__ == '__main__' or not CONFIG[BFA_Settings]['client']:
    main()
