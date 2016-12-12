# -*- coding: utf-8 -*-

#             __
# _|_ o __  _  _) __ _  |  _
#  |_ | |||(/_/__ | (/_ | (_|><
#

import json
import os

from requests import Session
from requests.compat import urljoin, quote
from six import iteritems

__version__ = '0.2.0'

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


class HTTPClient(object):
    """Base HTTP client (Requests HTTP library).

    Provides a :class:`requests.Session` with cookie persistence.
    """

    def __init__(self):
        self.session = Session()

    def request(self, method, url, **kwargs):
        """Constructs a :class:`requests.Request` and sends it.

        :param method: method for the new :class:`requests.Request` object.
        :param url: URL for the new :class:`requests.Request` object.
        :param kwargs: Optional :class:`requests.Request` arguments.

        :rtype: requests.Response
        """

        res = self.session.request(method, url, **kwargs)

        # Raises a :class:`CouchDbError` exception
        if not (200 <= res.status_code < 400):
            try:
                message = res.json()
            except ValueError:
                message = None
            ex_args = (message, res)

            if res.status_code == 400:
                raise BadRequest(*ex_args)
            if res.status_code == 401:
                raise Unauthorized(*ex_args)
            if res.status_code == 403:
                raise Forbidden(*ex_args)
            if res.status_code == 404:
                raise ResourceNotFound(*ex_args)
            if res.status_code == 405:
                raise MethodNotAllowed(*ex_args)
            if res.status_code == 409:
                raise ResourceConflict(*ex_args)
            if res.status_code == 412:
                raise PreconditionFailed(*ex_args)
            if res.status_code == 500:
                raise ServerError(*ex_args)

            raise CouchDbError(*ex_args)

        return res


class Server(object):
    """Representation of a CouchDB server."""

    def __init__(self, url=COUCHDB_URL):
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

        data = {'name': username, 'password': password}
        return self.request('POST', '_session', json=data)

    # http://docs.couchdb.org/en/latest/api/database/compact.html#post--db-_compact
    def compact(self, name, ddoc=None):
        """Starts compaction for a database or ddoc.

        :param name: The name of the database.
        :param ddoc: TODO: Document
        """

        path = os.path.join('_compact', ddoc) if ddoc else '_compact'
        return self.request('POST', name, path, json={})

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

        data = {'source': name, 'target': target}
        data.update(options) if options else None
        return self.request('POST', '_replicate', json=data)

    # http://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
    def session(self):
        """Returns Cookie-based login information."""

        return self.request('GET', '_session')

    def request(self, method, name=None, path=None, **kwargs):
        """Constructs a :class:`requests.Request` and sends it.

        :rtype: requests.Response
        """

        # http://wiki.apache.org/couchdb/HTTP_database_API#Naming_and_Addressing
        if name and not name.startswith('_'):
            # Special CouchDB components
            name = quote(name, "~()*!.\'")

        if name and path:
            path = os.path.join(name, str(path))  # handle numeric paths
        elif name:
            path = name

        url = urljoin(self.url, path)

        # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
        if 'params' in kwargs and kwargs['params']:
            p = kwargs['params'].copy()  # mutable!
            # Search parameters must be JSON-encoded
            for i in ('startkey', 'endkey', 'key', 'keys'):
                if i in p:
                    p[i] = json.dumps(p[i])
            # And Python titlecased booleans
            for k, v in iteritems(p):
                if v is True or v is False:
                    p[k] = json.dumps(v)
            kwargs['params'] = p

        return self.client.request(method, url, **kwargs)


class Database(object):
    """Representation of a CouchDB database."""

    def __init__(self, server, name):
        self.server = server
        self.name = name

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.name)

    # http://docs.couchdb.org/en/latest/api/document/common.html#put--db-docid
    # http://docs.couchdb.org/en/latest/api/database/common.html#post--db
    def insert(self, doc, params=None):
        """Inserts or updates a document.

        :param doc: The document to insert.
        :param params: Optional query parameters.
        """

        method = 'PUT' if '_id' in doc else 'POST'
        path = doc['_id'] if '_id' in doc else None
        return self._request(method, path, params=params, json=doc)

    # http://docs.couchdb.org/en/latest/api/document/common.html#delete--db-docid
    def delete(self, doc):
        """Deletes a document.

        :param doc: A dict of the document ``_id`` and ``_rev``.
        """

        params = {'rev': doc['_rev']}
        return self._request('DELETE', doc['_id'], params=params)

    # http://docs.couchdb.org/en/latest/api/document/common.html#get--db-docid
    def get(self, _id, params=None):
        """Returns a document.

        :param _id: The name of the document.
        :param params: Optional query parameters.
        """

        return self._request('GET', _id, params=params)

    # http://docs.couchdb.org/en/latest/api/document/common.html#head--db-docid
    def head(self, _id):
        """Returns the HTTP headers of a document.

        :param _id: The name of the document.
        """

        return self._request('HEAD', _id)

    # http://docs.couchdb.org/en/latest/api/database/bulk-api.html#post--db-_bulk_docs
    def bulk(self, docs, options=None):
        """Inserts or updates multiple documents in a single request.

        :param docs: A sequence of document objects.
        :param options: Optional bulk arguments.
        """

        data = {'docs': docs}
        data.update(options) if options else None
        return self._request('POST', '_bulk_docs', json=data)

    # http://docs.couchdb.org/en/latest/api/database/bulk-api.html#get--db-_all_docs
    def list(self, params=None):
        """Returns a built-in view of all documents.

        :param params: Optional query parameters.
        """

        return self._request('GET', '_all_docs', params=params)

    def view(self, ddoc, _type, view, params=None):

        # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
        if params:
            p = params.copy()  # mutable!
            # Search parameters must be JSON-encoded
            for i in ('counts', 'drilldown', 'group_sort', 'ranges', 'sort'):
                if i in p:
                    p[i] = json.dumps(p[i])
            params = p

        type_ = '_{0}'.format(_type)
        path = os.path.join('_design', ddoc, type_, view)
        return self._request('GET', path, params=params)

    def ddoc_list(self, ddoc, view, _list, params=None):

        return self.view(ddoc, 'list', os.path.join(_list, view), params)

    def ddoc_show(self, ddoc, view, _id, params=None):

        return self.view(ddoc, 'show', os.path.join(view, _id), params)

    # http://docs.couchdb.org/en/latest/api/document/attachments.html#put--db-docid-attname
    def att_insert(self, doc, att_name, att, content_type):
        """Inserts an attachment.

        :param doc: A dict of the document ``_id`` and ``_rev``.
        :param att_name: The name of the attachment.
        :param att: The attachment to insert.
        :param content_type: The attachment MIME type.

        :rtype: requests.Response
        """

        path = os.path.join(doc['_id'], att_name)
        params = {'rev': doc['_rev']}
        h = {'Content-Type': content_type}
        return self._request('PUT', path, params=params, data=att, headers=h)

    # http://docs.couchdb.org/en/latest/api/document/attachments.html#delete--db-docid-attname
    def att_delete(self, doc, att_name):
        """Deletes an attachment.

        :param doc: A dict of the document ``_id`` and ``_rev``.
        :param att_name: The name of the attachment.

        :rtype: requests.Response
        """

        path = os.path.join(doc['_id'], att_name)
        params = {'rev': doc['_rev']}
        return self._request('DELETE', path, params=params)

    # http://docs.couchdb.org/en/latest/api/document/attachments.html#get--db-docid-attname
    def att_get(self, doc, att_name):
        """Returns an attachment.

        :param doc: A dict of the document ``_id`` and ``_rev``.
        :param att_name: The name of the attachment.

        :rtype: requests.Response
        """

        path = os.path.join(doc['_id'], att_name)
        params = {'rev': doc['_rev']} if '_rev' in doc else None
        return self._request('GET', path, params=params)

    # http://docs.couchdb.org/en/latest/api/document/attachments.html#head--db-docid-attname
    def att_head(self, doc, att_name):
        """Returns the HTTP headers of an attachment.

        :param doc: A dict of the document ``_id`` and ``_rev``.
        :param att_name: The name of the attachment.

        :rtype: requests.Response
        """

        path = os.path.join(doc['_id'], att_name)
        params = {'rev': doc['_rev']} if '_rev' in doc else None
        return self._request('HEAD', path, params=params)

    def _request(self, method, path=None, **kwargs):
        """Constructs and sends a request."""

        return self.server.request(method, self.name, path, **kwargs)


class CouchDbError(Exception):
    """Class for errors based on HTTP status codes >= 400."""

    def __init__(self, message, response):
        """Initialize the error object."""

        super(CouchDbError, self).__init__(message)
        self.response = response


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class BadRequest(CouchDbError):
    """Exception raised when a 400 HTTP error is received."""


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class Unauthorized(CouchDbError):
    """Exception raised when a 401 HTTP error is received."""


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class Forbidden(CouchDbError):
    """Exception raised when a 403 HTTP error is received."""


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class ResourceNotFound(CouchDbError):
    """Exception raised when a 404 HTTP error is received."""


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class MethodNotAllowed(CouchDbError):
    """Exception raised when a 405 HTTP error is received."""


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class ResourceConflict(CouchDbError):
    """Exception raised when a 409 HTTP error is received."""


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class PreconditionFailed(CouchDbError):
    """Exception raised when a 412 HTTP error is received."""


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class ServerError(CouchDbError):
    """Exception raised when a 500 HTTP error is received."""
