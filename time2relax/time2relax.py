# -*- coding: utf-8 -*-

import os

from .clients import HTTPClient
from .compat import urljoin

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


class Server(object):
    """Representation of a CouchDB server."""

    def __init__(self, url=COUCHDB_URL):
        """Initialize the server object."""

        self._c = HTTPClient()
        self.url = url

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.url)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
    def auth(self, username, password):
        """Authenticates user by Cookie-based user login."""

        url = urljoin(self.url, '_session')
        data = {'name': username, 'password': password}

        return self.request('POST', url, json=data)

    # http://docs.couchdb.org/en/latest/api/database/compact.html#post--db-_compact
    def compact(self, name, ddoc=None):
        """Starts a compaction for the database or ddoc."""

        url = '/'.join([urljoin(self.url, name), '_compact'])
        if ddoc:
            url = '/'.join([url, ddoc])

        return self.request('POST', url, json={})

    # http://docs.couchdb.org/en/latest/api/database/common.html#put--db
    def create(self, name):
        """Creates a new database."""

        url = urljoin(self.url, name)

        return self.request('PUT', url)

    # http://docs.couchdb.org/en/latest/api/database/common.html#delete--db
    def delete(self, name):
        """Deletes an existing database."""

        url = urljoin(self.url, name)

        return self.request('DELETE', url)

    # http://docs.couchdb.org/en/latest/api/database/common.html#get--db
    def get(self, name):
        """Returns the database information."""

        url = urljoin(self.url, name)

        return self.request('GET', url)

    # http://docs.couchdb.org/en/latest/api/server/common.html#get--_all_dbs
    def list(self):
        """Returns a list of all the databases."""

        url = urljoin(self.url, '_all_dbs')

        return self.request('GET', url)

    # http://docs.couchdb.org/en/latest/api/server/common.html#replicate
    def replicate(self, name, target, options=None):
        """Starts or cancels the replication."""

        url = urljoin(self.url, '_replicate')
        data = {'source': name, 'target': target}
        if options:
            data.update(options)

        return self.request('POST', url, json=data)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
    def session(self):
        """Returns Cookie-based login user information."""

        url = urljoin(self.url, '_session')

        return self.request('GET', url)

    def request(self, method, url, **kwargs):
        """Constructs and sends a request."""


        # Pipe to the HTTP client
        return self.client.request(method, u, **k)


class Database(object):
    """Representation of a CouchDB database."""

    def __init__(self, server, name):
        """Initialize the database object."""

        self._s = server
        self.name = name
        self.url = urljoin(server.url, name)

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.url)

    def request(self, method, url, **kwargs):
        """Constructs and sends a request."""

        # Just relax!
        return self._s.request(method, url, **kwargs)





