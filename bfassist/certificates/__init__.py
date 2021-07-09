#############################################################################
#
#
#   BFA SSL-Certificates Manager
#
#
#############################################################################
""" This provides a small manager for generating and administrating the ssl certificates used by bfa. Well, currently
it just generates ssl certificates for bfa, nothing special. In the future I would like to add further features if I do
not find a better alternate package. A start would probably be to integrate it with the database.

    Dependencies:

        2nd-party-dependency: (py)OpenSSL

        note::  Author(s): Mitch last-check: 07.07.2021 """

from os import mkdir
from os.path import exists

from OpenSSL import crypto


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def generateCert(email: str = None, common: str = None, country: str = None, locality: str = None,
                 state: str = None, organization: str = None, unit: str = None, serial: int = 0,
                 start: int = 0, end: int = 10 * 365 * 24 * 60 * 60, pem: str = None):
    """ Function to generate a self-signed cert and key.

        :return: Path to a pem-file containing key and certificate.

            note:: Author(s): Mitch """

    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = country
    cert.get_subject().ST = state
    cert.get_subject().L = locality
    cert.get_subject().O = organization
    cert.get_subject().OU = unit
    cert.get_subject().CN = common
    cert.get_subject().emailAddress = email
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(start)
    cert.gmtime_adj_notAfter(end)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)

    # for some reason the 'sign' function type-hints at bytes, but actually requires a string since it uses decode on it
    # noinspection PyTypeChecker
    cert.sign(k, 'sha512')
    with open('bfassist/certificates/' + pem + '_bfa.key', "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open('bfassist/certificates/' + pem + '_bfa.crt', "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
    with open('bfassist/certificates/' + pem + '_bfa.pem', "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

    return 'bfassist/certificates/' + pem + '_bfa.pem'
