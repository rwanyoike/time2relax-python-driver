# -*- coding: utf-8 -*-

from urllib import quote


def encode_url_database(url):
    """Encodes a database url."""

    # http://wiki.apache.org/couchdb/HTTP_database_API#Naming_and_Addressing
    return quote(url, "~()*!.\'")


def format_url_params(params):
    """Formats sent url params."""

    p = {}

    for k, v in params.items():
        if type(v) is str:
            v = '"{0}"'.format(v)
        elif v is True:
            v = 'true'
        elif v is False:
            v = 'false'
        p[k] = v

    return p
