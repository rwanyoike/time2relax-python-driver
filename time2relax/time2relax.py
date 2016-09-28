# -*- coding: utf-8 -*-

import json
import os
from urllib import quote
from urlparse import urljoin

from requests import Session

from .exceptions import (BadRequest, CouchDbError, Forbidden, MethodNotAllowed,
                         PreconditionFailed, ResourceConflict,
                         ResourceNotFound, ServerError, Unauthorized)

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


class HTTPClient(object):
    """Base HTTP client. (Requests HTTP library)

    Provides a :class:`requests.Session` with cookie persistence.
    """

    def __init__(self):
        """Initialize the HTTP client object."""

        # Session with cookie persistence
        self.session = Session()

    def request(self, method, url, **kwargs):
        """Constructs a :class:`requests.Request` and sends it.

        :param method: method for the new :class:`requests.Request` object.
        :param url: URL for the new :class:`requests.Request` object.
        :param kwargs: Optional :class:`requests.Request` arguments.

        :rtype: requests.Response
        """

        r = self.session.request(method, url, **kwargs)

        if not (200 <= r.status_code < 400):
            self._handle_error(r)

        return r

    def _handle_error(self, response):
        """Raises a :class:`CouchDbError` exception.

        :param response: The :class:`requests.Response` object.
        """

        try:
            message = response.json()
        except ValueError:
            message = None

        args = (message, response)

        if response.status_code == 400:
            raise BadRequest(*args)
        if response.status_code == 401:
            raise Unauthorized(*args)
        if response.status_code == 403:
            raise Forbidden(*args)
        if response.status_code == 404:
            raise ResourceNotFound(*args)
        if response.status_code == 405:
            raise MethodNotAllowed(*args)
        if response.status_code == 409:
            raise ResourceConflict(*args)
        if response.status_code == 412:
            raise PreconditionFailed(*args)
        if response.status_code == 500:
            raise ServerError(*args)

        raise CouchDbError(*args)


class Server(object):
    """Representation of a CouchDB server."""

    def __init__(self, url=COUCHDB_URL):
        """Initialize the server object.

        :param url: URL for the CouchDB instance.
        """

        self.client = HTTPClient()
        self.url = url

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.url)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
    def auth(self, username, password):
        """Authenticates user by Cookie-based login.

        :param username: Username.
        :param password: Password.
        """

        data = {
            'name': username,
            'password': password,
        }

        return self.request('POST', '_session', json=data)

    # http://docs.couchdb.org/en/latest/api/database/compact.html#post--db-_compact
    def compact(self, name, ddoc=None):
        """Starts compaction for a database or ddoc.

        :param name: The name of the database.
        :param ddoc: TODO
        """

        url = '_compact'

        if ddoc:
            url = os.path.join(url, ddoc)

        return self.request('POST', name, url, json={})

    # http://docs.couchdb.org/en/latest/api/database/common.html#put--db
    def create(self, name):
        """Creates a new database.

        :param name: The name of the database.
        """

        return self.request('PUT', name)

    # http://docs.couchdb.org/en/latest/api/database/common.html#delete--db
    def delete(self, name):
        """Deletes an existing database.

        :param name: The name of the database.
        """

        return self.request('DELETE', name)

    # http://docs.couchdb.org/en/latest/api/database/common.html#get--db
    def get(self, name):
        """Returns the database information.

        :param name: The name of the database.
        """

        return self.request('GET', name)

    # http://docs.couchdb.org/en/latest/api/server/common.html#get--_all_dbs
    def list(self):
        """Returns a list of all databases."""

        return self.request('GET', '_all_dbs')

    # http://docs.couchdb.org/en/latest/api/server/common.html#replicate
    def replicate(self, name, target, options=None):
        """Starts or cancels a replication.

        :param name: URL or name of the source database.
        :param target: URL or name of the target database.
        :param options: Optional replication arguments.
        """

        data = {
            'source': name,
            'target': target,
        }

        if options:
            data.update(options)

        return self.request('POST', '_replicate', json=data)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
    def session(self):
        """Returns Cookie-based login information."""

        return self.request('GET', '_session')

    def request(self, method, name=None, url=None, **kwargs):
        """Constructs a :class:`requests.Request` and sends it.

        :rtype: requests.Response
        """

        # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
        # Several search parameters must be JSON-encoded
        if 'params' in kwargs and kwargs['params']:
            for i in ('startkey', 'endkey', 'key', 'keys'):
                if i in kwargs['params']:
                    kwargs['params'][i] = json.dumps(kwargs['params'][i])
            # Python booleans
            for k, v in kwargs['params'].iteritems():
                if v is True or v is False:
                    kwargs['params'][k] = json.dumps(v)

        # http://wiki.apache.org/couchdb/HTTP_database_API#Naming_and_Addressing
        if name:
            # Avoid special components
            if not name.startswith('_'):
                name = quote(name, "~()*!.\'")
            if url:
                url = os.path.join(name, url)
            else:
                url = name

        url = urljoin(self.url, url)

        # Pipe to the HTTP client
        return self.client.request(method, url, **kwargs)


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

    def view(self, ddoc, _type, view, params=None):

        # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
        # Several search parameters must be JSON-encoded
        if params:
            for i in ('counts', 'drilldown', 'group_sort', 'ranges', 'sort'):
                if i in params:
                    params[i] = json.dumps(params[i])

        url = os.path.join('_design', ddoc, '_{0}'.format(_type), view)

        return self.request('GET', url, params=params)

    def ddoc_list(self, ddoc, view, _list, params=None):

        return self.view(ddoc, 'list', os.path.join(_list, view), params)

    def ddoc_show(self, ddoc, view, _id, params=None):

        return self.view(ddoc, 'show', os.path.join(view, _id), params)

    def request(self, method, url=None, **kwargs):
        """Constructs and sends a request."""

        return self.server.request(method, self.name, url, **kwargs)
