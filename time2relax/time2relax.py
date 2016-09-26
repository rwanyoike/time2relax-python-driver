# -*- coding: utf-8 -*-

import os
from urllib import quote
from urlparse import urljoin

from .clients import HTTPClient

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


class Server(object):
    """Representation of a CouchDB server."""

    def __init__(self, url=COUCHDB_URL):
        """Initialize the server object."""

        self.client = HTTPClient()
        self.url = url

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.url)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
    def auth(self, username, password):
        """Authenticates user by Cookie-based user login."""

        data = {
            'name': username,
            'password': password,
        }

        return self.request('POST', '_session', json=data)

    # http://docs.couchdb.org/en/latest/api/database/compact.html#post--db-_compact
    def compact(self, name, ddoc=None):
        """Starts a compaction for the database or ddoc."""

        url = os.path.join(encode_url_database(name), '_compact')

        if ddoc:
            url = os.path.join(url, ddoc)

        return self.request('POST', url, json={})

    # http://docs.couchdb.org/en/latest/api/database/common.html#put--db
    def create(self, name):
        """Creates a new database."""

        return self.request('PUT', encode_url_database(name))

    # http://docs.couchdb.org/en/latest/api/database/common.html#delete--db
    def delete(self, name):
        """Deletes an existing database."""

        return self.request('DELETE', encode_url_database(name))

    # http://docs.couchdb.org/en/latest/api/database/common.html#get--db
    def get(self, name):
        """Returns the database information."""

        return self.request('GET', encode_url_database(name))

    # http://docs.couchdb.org/en/latest/api/server/common.html#get--_all_dbs
    def list(self):
        """Returns a list of all the databases."""

        return self.request('GET', '_all_dbs')

    # http://docs.couchdb.org/en/latest/api/server/common.html#replicate
    def replicate(self, name, target, options=None):
        """Starts or cancels the replication."""

        data = {
            'source': name,
            'target': target,
        }

        if options:
            data.update(options)

        return self.request('POST', '_replicate', json=data)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
    def session(self):
        """Returns Cookie-based login user information."""

        return self.request('GET', '_session')

    def request(self, method, url, **kwargs):
        """Constructs and sends a request."""

        u = urljoin(self.url, url)
        k = kwargs

        if 'params' in kwargs and kwargs['params']:
            k['params'] = format_url_params(kwargs['params'])

        # Pipe to the HTTP client
        return self.client.request(method, u, **k)


class Database(object):
    """Representation of a CouchDB database."""

    def __init__(self, server, name):
        """Initialize the database object."""

        self.name = name
        self.server = server
        self.url = urljoin(server.url, name)

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.name)

    # http://docs.couchdb.org/en/latest/api/document/common.html#put--db-docid
    # http://docs.couchdb.org/en/latest/api/database/common.html#post--db
    def insert(self, doc, params=None):
        """Creates or updates a document."""

        if '_id' in doc:
            method = 'PUT'
            url = doc['_id']
        else:
            method = 'POST'
            url = None

        return self.request(method, url, params=params, json=doc)

    # http://docs.couchdb.org/en/latest/api/document/common.html#delete--db-docid
    def delete(self, _id, rev):
        """Deletes the document."""

        return self.request('DELETE', _id, params={'rev': rev})

    # http://docs.couchdb.org/en/latest/api/document/common.html#get--db-docid
    def get(self, _id, params=None):
        """Returns the document."""

        return self.request('GET', _id, params=params)

    # http://docs.couchdb.org/en/latest/api/document/common.html#head--db-docid
    def head(self, _id):
        """Returns bare information in the HTTP Headers for the document."""

        return self.request('HEAD', _id)

    # http://docs.couchdb.org/en/latest/api/database/bulk-api.html#post--db-_bulk_docs
    def bulk(self, docs, options=None):
        """Inserts or updates multiple documents in to the database in a single
        request."""

        data = {'docs': docs}

        if options:
            data.update(options)

        return self.request('POST', '_bulk_docs', json=data)

    # http://docs.couchdb.org/en/latest/api/database/bulk-api.html#get--db-_all_docs
    def list(self, params=None):
        """Returns a built-in view of all documents in this database."""

        return self.request('GET', '_all_docs', params=params)

    def request(self, method, url=None, **kwargs):
        """Constructs and sends a request."""

        u = encode_url_database(self.name)

        if url:
            u = os.path.join(u, url)

        return self.server.request(method, u, **kwargs)


# http://wiki.apache.org/couchdb/HTTP_database_API#Naming_and_Addressing
def encode_url_database(url):
    """Encodes a database url."""

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
