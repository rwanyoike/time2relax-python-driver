# -*- coding: utf-8 -*-

import os

from requests.compat import urljoin

from .clients import HTTPClient

BASE_CLIENT = HTTPClient
COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


class Server(object):
    """Representation of a CouchDB server."""

    def __init__(self, url=COUCHDB_URL):
        """Initialize the server object."""

        self._c = BASE_CLIENT()
        self.url = url

    def __repr__(self):
        return '<{0} [{1}]>'.format(type(self).__name__, self.url)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
    def auth(self, username, password):
        """Authenticates user by Cookie-based user login."""

        url = urljoin(self.url, '_session')
        data = {'name': username, 'password': password}
        self.request('POST', url, json=data)

    # http://docs.couchdb.org/en/latest/api/database/compact.html#post--db-_compact
    def compact(self, name, ddoc=None):
        """Starts a compaction for the database or selected design document."""

        url = '/'.join([urljoin(self.url, name), '_compact'])
        if ddoc:
            url = '/'.join([url, ddoc])
        self.request('POST', url, json={})

    # http://docs.couchdb.org/en/latest/api/database/common.html#put--db
    def create(self, name):
        """Creates a new database."""

        url = urljoin(self.url, name)
        self.request('PUT', url)

        return Database(self, name)

    # http://docs.couchdb.org/en/latest/api/database/common.html#delete--db
    def delete(self, name):
        """Deletes an existing database."""

        url = urljoin(self.url, name)
        self.request('DELETE', url)

    # http://docs.couchdb.org/en/latest/api/database/common.html#get--db
    def get(self, name):
        """Returns the database information."""

        url = urljoin(self.url, name)
        j, _ = self.request('GET', url)

        return j

    # http://docs.couchdb.org/en/latest/api/server/common.html#get--_all_dbs
    def list(self):
        """Returns a list of all the databases."""

        url = urljoin(self.url, '_all_dbs')
        j, _ = self.request('GET', url)

        for i in j:
            yield Database(self, i)

    # http://docs.couchdb.org/en/latest/api/server/common.html#replicate
    def replicate(self, name, target, options=None):
        """Starts or cancels the replication."""

        url = urljoin(self.url, '_replicate')
        data = {'source': name, 'target': target}
        if options:
            data.update(options)
        j, _ = self.request('POST', url, json=data)

        return j

    # http://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
    def session(self):
        """Returns Cookie-based login user information."""

        url = urljoin(self.url, '_session')
        j, _ = self.request('GET', url)

        return j

    def request(self, method, url, **kwargs):
        """Constructs and sends a request."""

        # Pipe to HTTP client
        return self._c.request(method, url, **kwargs)


class Database(object):
    """Representation of a CouchDB database."""

    def __init__(self, server, name):
        """Initialize the database object."""

        self._s = server
        self.name = name
        self.url = urljoin(server.url, name)

    def __repr__(self):
        return '<{0} [{1}]>'.format(type(self).__name__, self.name)

    def request(self, method, url, **kwargs):
        """Constructs and sends a request."""

        # Pipe to HTTP client
        return self._s.request(method, url, **kwargs)


class Document(dict):
    """Representation of a CouchDB document."""

    def __repr__(self):
        return '<{0} [{1}@{2}]>'.format(type(self).__name__, self.id, self.rev)

    @property
    def id(self):
        """Returns the document _id."""

        return self.get('_id')

    @property
    def rev(self):
        """Returns the document _rev."""

        return self.get('_rev')

