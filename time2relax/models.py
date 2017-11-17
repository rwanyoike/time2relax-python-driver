# -*- coding: utf-8 -*-

"""
time2relax.models
~~~~~~~~~~~~~~~~~

This module contains the primary objects that power time2relax.
"""

from json import dumps
from posixpath import join as urljoin

from requests import Session
from six import iteritems

from .exceptions import (
    BadRequest, ResourceConflict, MethodNotAllowed, ServerError,
    ResourceNotFound, Unauthorized, Forbidden, PreconditionFailed,
    CouchDBError)
from .utils import (
    encode_att_id, handle_query_args, encode_doc_id, get_database_host,
    get_database_name)

_LIST = '_list'
_SHOW = '_show'
_VIEW = '_view'


class CouchDB(object):
    """Representation of a CouchDB database.

    Provides URL-parameter encoding, modeled Exceptions, a Requests session,
    and database initialization.

    Basic usage::

        >>> import time2relax
        >>> db = time2relax.CouchDB('http://localhost:5984/testdb')
        >>> db.insert({'title': 'Ziggy Stardust'})
        <Response [201]>
    """

    def __init__(self, url, create_database=True):
        """Initialize the database object.

        :param url: Database URL.
        :param create_database: (optional) Set to True by default.
        """

        # Database created, destroyed
        self._created, self._destroyed = False, False

        #: CouchDB database host
        self.host = get_database_host(url)

        #: CouchDB database name
        self.name = get_database_name(url)

        #: CouchDB database URL
        self.url = urljoin(self.host, self.name)

        #: Handle database initialization
        self.create_database = create_database

        #: Default requests.Session
        self.session = Session()
        #: http://docs.couchdb.org/en/stable/api/basics.html#request-headers
        self.session.headers['Accept'] = 'application/json'

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.url)

    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_all_docs
    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs
    def all_docs(self, params=None, **kwargs):
        """Fetch multiple documents.

        :param params: (optional) Dictionary of URL parameters to append to the
            URL.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        method, kwargs2 = handle_query_args(params)
        kwargs.update(kwargs2)

        return self.request(method, '_all_docs', **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_bulk_docs
    def bulk_docs(self, docs, json=None, **kwargs):
        """Create, update or delete multiple documents.

        :param docs: Sequence of document objects to be sent.
        :param json: (optional) JSON to send in the body of the
            :class:`requests.Request`.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        kwargs['json'] = {} if not json else json
        kwargs['json'].update({'docs': docs})

        return self.request('POST', '_bulk_docs', **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact
    def compact(self, **kwargs):
        """Trigger a compaction operation.

        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if 'json' not in kwargs:
            kwargs['json'] = {}  # Set application/json

        return self.request('POST', '_compact', **kwargs)

    # http://docs.couchdb.org/en/stable/api/ddoc/render.html#get--db-_design-ddoc-_list-func-view
    def ddoc_list(self, ddoc_id, func_id, view_id, other_id=None, **kwargs):
        """Apply a list function against a view.

        :param ddoc_id: Design document name.
        :param func_id: List function name.
        :param view_id: View function name.
        :param other_id: Other design document name that holds the view
            function.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if other_id:
            path = urljoin(encode_doc_id(other_id), view_id)
        else:
            path = view_id

        return self._ddoc('GET', ddoc_id, _LIST, func_id, path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/ddoc/render.html#get--db-_design-ddoc-_show-func
    def ddoc_show(self, ddoc_id, func_id, doc_id=None, **kwargs):
        """Apply a show function against a document.

        :param ddoc_id: Design document name.
        :param func_id: Show function name.
        :param doc_id: Document ``_id`` to execute the show function on.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if doc_id:
            path = encode_doc_id(doc_id)
        else:
            path = None

        return self._ddoc('GET', ddoc_id, _SHOW, func_id, path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/ddoc/views.html#get--db-_design-ddoc-_view-view
    def ddoc_view(self, ddoc_id, func_id, params=None, **kwargs):
        """Execute a view function.

        :param ddoc_id: Design document name.
        :param func_id: View function name.
        :param params: (optional) Dictionary of URL parameters to append to the
            URL.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        method, kwargs2 = handle_query_args(params)
        kwargs.update(kwargs2)

        return self._ddoc(method, ddoc_id, _VIEW, func_id, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#delete--db
    def destroy(self, **kwargs):
        """Delete the database.

        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        try:
            # Don't setup the database
            return self.request('DELETE', create_database=False, **kwargs)
        finally:
            # Prevent further requests
            self._destroyed = True

    # http://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
    def get(self, doc_id, params=None, **kwargs):
        """Retrieve a document.

        :param doc_id: Document ``_id`` to retrieve.
        :param params: (optional) Dictionary of URL parameters to append to the
            URL.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if params and 'open_revs' in params:
            # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
            if params['open_revs'] != 'all':
                params = params.copy()
                params['open_revs'] = dumps(params['open_revs'])

        path = encode_doc_id(doc_id)
        kwargs['params'] = params

        return self.request('GET', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/attachments.html#get--db-docid-attname
    def get_att(self, doc_id, att_id, **kwargs):
        """Retrieve an attachment.

        :param doc_id: Document ``_id`` of attachment.
        :param att_id: Attachment name to retrieve.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        path = urljoin(encode_doc_id(doc_id), encode_att_id(att_id))

        return self.request('GET', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#get--db
    def info(self, **kwargs):
        """Get information about the database.

        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        return self.request('GET', **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
    # http://docs.couchdb.org/en/stable/api/database/common.html#post--db
    def insert(self, doc, **kwargs):
        """Create or update an existing document.

        :param doc: Document dictionary to insert.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if '_id' in doc:
            method = 'PUT'
            path = encode_doc_id(doc['_id'])
        else:
            method = 'POST'
            path = ''

        kwargs['json'] = doc  # replace

        return self.request(method, path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/attachments.html#put--db-docid-attname
    def insert_att(self, doc_id, doc_rev, att_id, att, att_type, **kwargs):
        """Create or update an existing attachment.

        :param doc_id: Document ``_id`` of attachment.
        :param doc_rev: Document revision. (Can be ``None``)
        :param att_id: Attachment name.
        :param att: Attachment dictionary, bytes, or file-like object to
            insert.
        :param att_type: Attachment MIME type.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if doc_rev:
            if 'params' not in kwargs:
                kwargs['params'] = {}
            kwargs['params']['rev'] = doc_rev
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        path = urljoin(encode_doc_id(doc_id), encode_att_id(att_id))
        kwargs['headers']['Content-Type'] = att_type
        kwargs['data'] = att  # replace

        return self.request('PUT', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
    def remove(self, doc_id, doc_rev, **kwargs):
        """Delete a document.

        :param doc_id: Document ``_id`` to remove.
        :param doc_rev: Document revision.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if 'params' not in kwargs:
            kwargs['params'] = {}

        path = encode_doc_id(doc_id)
        kwargs['params']['rev'] = doc_rev

        return self.request('DELETE', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/attachments.html#delete--db-docid-attname
    def remove_att(self, doc_id, doc_rev, att_id, **kwargs):
        """Delete an attachment.

        :param doc_id: Document ``_id`` of attachment.
        :param doc_rev: Document revision.
        :param att_id: Attachment name to remove.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if 'params' not in kwargs:
            kwargs['params'] = {}

        path = urljoin(encode_doc_id(doc_id), encode_att_id(att_id))
        kwargs['params']['rev'] = doc_rev

        return self.request('DELETE', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/server/common.html#replicate
    def replicate_to(self, target, json=None, **kwargs):
        """Replicate data from source (this) to target.

        :param target: URL or name of the target database.
        :param json: (optional) JSON to send in the body of the
            :class:`requests.Request`.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        url = urljoin(self.host, '_replicate')
        kwargs['json'] = {} if not json else json
        kwargs['json'].update({
            'source': self.url,
            'target': target,
        })

        return self._request('POST', url, **kwargs)

    def request(self, method, path='', create_database=True, **kwargs):
        """Construct a :class:`requests.Request` object and send it.

        :param method: Method for the new :class:`requests.Request` object.
        :param path: Path to add to the :class:`requests.Request` URL.
        :param create_database: Setup the database.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if self._destroyed:
            raise CouchDBError('Database is destroyed')

        url = urljoin(self.url, path)

        # Check if the database exists or create it
        if create_database and self.create_database:
            if not self._created:
                try:
                    self._request('HEAD', self.url)
                except ResourceNotFound:
                    self._request('PUT', self.url)
                self._created = True

        return self._request(method, url, **kwargs)

    def _ddoc(self, method, ddoc_id, func_type, func_id, extra=None, **kwargs):
        """Apply or execute a design document function.

        :param method: Method for the new :class:`requests.Request` object.
        :param ddoc_id: Design document name.
        :param func_type: Function type.
        :param func_id: Function name.
        :param extra: FIXME: What is this?
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        doc_id = urljoin('_design', ddoc_id)
        path = urljoin(encode_doc_id(doc_id), func_type, func_id)

        if extra:
            path = urljoin(path, extra)

        return self.request(method, path, **kwargs)

    def _request(self, method, url, **kwargs):
        """Construct a request, prepare it and send it."""

        # Prepare the params dictionary
        if 'params' in kwargs and kwargs['params']:
            params = kwargs['params'].copy()  # mutable!
            for key, val in iteritems(params):
                # Handle Python titlecase booleans
                if type(val) == bool:
                    params[key] = dumps(val)
            kwargs['params'] = params

        r = self.session.request(method, url, **kwargs)
        if 200 <= r.status_code < 300:
            return r

        try:
            message = r.json()
        except ValueError:
            message = None

        # Raise a CouchDBError on a bad HTTP response
        errors = {
            400: BadRequest,
            401: Unauthorized,
            403: Forbidden,
            404: ResourceNotFound,
            405: MethodNotAllowed,
            409: ResourceConflict,
            412: PreconditionFailed,
            500: ServerError,
        }

        # http://docs.couchdb.org/en/stable/api/basics.html?#http-status-codes
        if r.status_code in errors:
            ex = errors[r.status_code]
            raise ex(message, r)

        raise CouchDBError(message, r)
