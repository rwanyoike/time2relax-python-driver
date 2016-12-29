# -*- coding: utf-8 -*-

#             __
# _|_ o __  _  _) __ _  |  _
#  |_ | |||(/_/__ | (/_ | (_|><
#

import os
from json import dumps

from requests import Session
from requests.compat import quote, urlparse, urlunparse
from six import iteritems

__version__ = '0.3.0'


class CouchDB(object):
    """Representation of a CouchDB database."""

    _destroyed = False
    _has_setup = False

    def __init__(self, name, skip_setup=False):
        """Initialize the database object.

        :param name: Database url to use.
        :param skip_setup: Don't check-create the database.
        """

        uri = urlparse(name)

        self.host = self._get_db_host(uri)
        self.name = self._get_db_name(uri)
        self.url = os.path.join(self.host, self.name)
        self.skip_setup = skip_setup
        self.session = Session()

        # http://docs.couchdb.org/en/stable/api/basics.html#request-headers
        self.session.headers['Accept'] = 'application/json'

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.url)

    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_all_docs
    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs
    def all_docs(self, params=None, **kwargs):
        """Fetch multiple documents.

        :param params: (optional) Dictionary of URL parameters to append to the
            URL.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        if not params:
            params = {}

        url = self._get_db_url('_all_docs')
        params = params.copy()  # mutable!

        if 'keys' in params:
            method = 'POST'
            kwargs['json'] = {'keys': params['keys']}  # hijack kwargs['json']
            params.pop('keys', None)
        else:
            method = 'GET'

        # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
        for i in ('start_key', 'startkey', 'end_key', 'endkey', 'key'):
            if i in params:
                params[i] = dumps(params[i])

        kwargs['params'] = params

        return self.request(method, url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_bulk_docs
    def bulk_docs(self, docs, json=None, **kwargs):
        """Create, update or delete multiple documents.

        :param docs: Sequence of document objects to be sent.
        :param json: (optional) JSON to send in the body of the ``request``.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        if not json:
            json = {}

        url = self._get_db_url('_bulk_docs')
        json.update({'docs': docs})

        kwargs['json'] = json

        return self.request('POST', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact
    def compact(self, **kwargs):
        """Trigger a compaction operation.

        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        url = self._get_db_url('_compact')

        if 'json' not in kwargs:
            # Set application/json content type
            kwargs['json'] = {}

        return self.request('POST', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#delete--db
    def destroy(self, **kwargs):
        """Delete the database.

        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        # Don't setup the database
        kwargs['_skip_setup'] = True
        response = self.request('DELETE', self.url, **kwargs)
        # Prevent further requests
        self._destroyed = True

        return response

    # http://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
    def get(self, doc_id, params=None, **kwargs):
        """Retrieve a document.

        :param doc_id: Document ``_id`` to retrieve.
        :param params: (optional) Dictionary of URL parameters to append to the
            URL.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        url = self._get_db_url(self._encode_doc_id(doc_id))

        if params and 'open_revs' in params:
            # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
            if params['open_revs'] != 'all':
                params = params.copy()  # mutable!
                params['open_revs'] = dumps(params['open_revs'])

        kwargs['params'] = params

        return self.request('GET', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/attachments.html#get--db-docid-attname
    def get_att(self, doc_id, att_id, **kwargs):
        """Retrieve an attachment.

        :param doc_id: Document ``_id`` of attachment.
        :param att_id: Attachment name to retrieve.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        url = self._get_db_url(os.path.join(self._encode_doc_id(doc_id),
                                            self._encode_att_id(att_id)))

        return self.request('GET', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#get--db
    def info(self, **kwargs):
        """Get information about the database.

        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('GET', self.url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
    # http://docs.couchdb.org/en/stable/api/database/common.html#post--db
    def insert(self, doc, **kwargs):
        """Create or update an existing document.

        :param doc: Document dictionary to insert.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        if '_id' in doc:
            method = 'PUT'
            url = self._get_db_url(self._encode_doc_id(doc['_id']))
        else:
            method = 'POST'
            url = self.url

        kwargs['json'] = doc  # hijack kwargs['json']

        return self.request(method, url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/attachments.html#put--db-docid-attname
    def insert_att(self, doc_id, att_id, doc_rev, att, _type, **kwargs):
        """Create or update an existing attachment.

        :param doc_id: Document ``_id`` of attachment.
        :param att_id: Attachment name to insert.
        :param doc_rev: Document revision. (Can be ``None``)
        :param att: Dictionary, bytes, or file-like object to send in the body
            of the ``request``.
        :param _type: Attachment MIME type.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        url = self._get_db_url(os.path.join(self._encode_doc_id(doc_id),
                                            self._encode_att_id(att_id)))

        if doc_rev:
            if 'params' not in kwargs:
                kwargs['params'] = {}
            kwargs['params']['rev'] = doc_rev

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Content-Type'] = _type
        kwargs['data'] = att

        return self.request('PUT', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
    def remove(self, doc_id, doc_rev, **kwargs):
        """Delete a document.

        :param doc_id: Document ``_id`` to remove.
        :param doc_rev: Document revision.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        url = self._get_db_url(self._encode_doc_id(doc_id))

        if 'params' not in kwargs:
            kwargs['params'] = {}

        kwargs['params']['rev'] = doc_rev

        return self.request('DELETE', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/attachments.html#delete--db-docid-attname
    def remove_att(self, doc_id, att_id, doc_rev, **kwargs):
        """Delete an attachment.

        :param doc_id: Document ``_id`` of attachment.
        :param att_id: Attachment name to remove.
        :param doc_rev: Document revision.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        url = self._get_db_url(os.path.join(self._encode_doc_id(doc_id),
                                            self._encode_att_id(att_id)))

        if 'params' not in kwargs:
            kwargs['params'] = {}

        kwargs['params']['rev'] = doc_rev

        return self.request('DELETE', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/server/common.html#replicate
    def replicate_to(self, target, json=None, **kwargs):
        """Replicate data from source (this) to target.

        :param target: URL or name of the target database.
        :param json: (optional) JSON to send in the body of the ``request``.
        :param kwargs: (optional) Arguments that ``request`` takes.
        :rtype: requests.Response
        """

        if json is None:
            json = {}

        url = os.path.join(self.host, '_replicate')
        data = {'source': self.url, 'target': target}
        json.update(data)

        kwargs['json'] = json

        return self.request('POST', url, **kwargs)

    def request(self, method, url, **kwargs):
        """Construct a :class:`requests.Request` object and send it.

        :param method: Method for the new :class:`requests.Request` object.
        :param url: URL for the new :class:`requests.Request` object.
        :param kwargs: Optional :class:`requests.Request` arguments.
        :rtype: requests.Response
        """

        if self._destroyed:
            raise CouchDBError('Database is destroyed')

        if '_skip_setup' in kwargs:
            kwargs.pop('_skip_setup')
        elif self.skip_setup or self._has_setup:
            pass  # skip!
        else:
            self._setup_database()

        if 'params' in kwargs and kwargs['params']:
            params = kwargs['params'].copy()  # mutable!
            self._prepare_params(params)
            kwargs['params'] = params

        return self._request(method, url, **kwargs)

    def _check_response(self, response):
        """Raise a :class:`CouchDBError` on a bad response."""

        if 200 <= response.status_code < 300:
            return

        exceptions = {
            400: BadRequest,
            401: Unauthorized,
            403: Forbidden,
            404: ResourceNotFound,
            405: MethodNotAllowed,
            409: ResourceConflict,
            412: PreconditionFailed,
            500: ServerError,
        }

        if response.status_code in exceptions:
            try:
                body = response.json()
                message = body['reason']
            except ValueError:
                message = None

            ex = exceptions[response.status_code]
            raise ex(message, response)

        raise CouchDBError(None, response)

    def _encode_att_id(self, att_id):
        """Encode an attachment id."""

        parts = map(self._encode_uri_component, att_id.split('/'))
        return '/'.join(parts)

    def _encode_doc_id(self, doc_id):
        """Encode a document id."""

        if doc_id.startswith('_design'):
            uri = self._encode_uri_component(doc_id[8:])
            return '_design/{0}'.format(uri)

        if doc_id.startswith('_local'):
            uri = self._encode_uri_component(doc_id[7:])
            return '_local/{0}'.format(uri)

        return self._encode_uri_component(doc_id)

    def _encode_uri_component(self, component):
        """Encode a uri component."""

        # http://stackoverflow.com/a/6618858/2497865
        return quote(component, "~()*!.\'")

    def _get_db_host(self, uri):
        """Get the database host from a uri."""

        data = (uri.scheme, uri.netloc, '', '', '', '')
        return urlunparse(data)

    def _get_db_name(self, uri):
        """Get the database name from a uri."""

        parts = uri.path.strip('/').split('/')
        db_name = parts.pop()

        # Prevent double encoding of the name
        if '%' not in db_name:
            db_name = self._encode_uri_component(db_name)

        return db_name

    def _get_db_url(self, path):
        """Build a database url from a path."""

        return os.path.join(self.url, path)

    def _prepare_params(self, params):
        """Prepare a ``params`` dictionary (mutable)."""

        for key, val in iteritems(params):
            # Handle Python titlecase booleans
            if type(val) == bool:
                params[key] = dumps(val)

    def _request(self, method, url, **kwargs):
        """Construct a request, prepare it and send it."""

        response = self.session.request(method, url, **kwargs)
        self._check_response(response)

        return response

    # http://docs.couchdb.org/en/stable/api/database/common.html#put--db
    def _setup_database(self):
        """Check if the database exists or create it."""

        try:
            self._request('HEAD', self.url)
        except ResourceNotFound:
            self._request('PUT', self.url)

        self._has_setup = True


class CouchDBError(Exception):
    """Class for errors based on bad HTTP status codes."""

    # http://docs.couchdb.org/en/stable/api/basics.html?#http-status-codes
    def __init__(self, message, response=None):
        """Initialize the exception object."""

        super(CouchDBError, self).__init__(message)
        self.response = response


class BadRequest(CouchDBError):
    """Exception raised when a 400 HTTP error is received."""


class Unauthorized(CouchDBError):
    """Exception raised when a 401 HTTP error is received."""


class Forbidden(CouchDBError):
    """Exception raised when a 403 HTTP error is received."""


class ResourceNotFound(CouchDBError):
    """Exception raised when a 404 HTTP error is received."""


class MethodNotAllowed(CouchDBError):
    """Exception raised when a 405 HTTP error is received."""


class ResourceConflict(CouchDBError):
    """Exception raised when a 409 HTTP error is received."""


class PreconditionFailed(CouchDBError):
    """Exception raised when a 412 HTTP error is received."""


class ServerError(CouchDBError):
    """Exception raised when a 500 HTTP error is received."""
