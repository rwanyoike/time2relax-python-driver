# -*- coding: utf-8 -*-

"""
time2relax.models
~~~~~~~~~~~~~~~~~

This module contains the primary objects that power time2relax.
"""

from json import dumps
from posixpath import join

from requests import Session
from requests.compat import urlparse
from six import iteritems

from .exceptions import ResourceNotFound
from .utils import (
    encode_att_id, encode_doc_id, get_db_host, get_db_name, get_http_exception, handle_query_args)

_LIST = '_list'
_SHOW = '_show'
_VIEW = '_view'


class CouchDB(object):
    """Representation of a CouchDB database.

    Provides URL-parameter encoding, modeled Exceptions, a Requests session,
    and database initialization.

    Example::

        >>> import time2relax
        >>> db = time2relax.CouchDB('http://localhost:5984/testdb')
        >>> db.insert({'title': 'Ziggy Stardust'})
        <Response [201]>
    """

    def __init__(self, url, create_db=True):
        """Initialize the database object.

        :param str url: Database URL.
        :param bool create_db: (optional) Create the database.
        """

        #: Database host
        self.host = get_db_host(url)

        #: Database name
        self.name = get_db_name(url)

        #: Database URL
        self.url = join(self.host, self.name)

        #: Database initialization
        self.create_db = create_db

        #: Default :class:`requests.Session`
        self.session = Session()
        # http://docs.couchdb.org/en/stable/api/basics.html#request-headers
        self.session.headers['Accept'] = 'application/json'

        #: Database created
        self._created = False

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.url)

    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_all_docs
    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs
    def all_docs(self, params=None, **kwargs):
        """Fetch multiple documents.

        :param params: (optional) Parameters to append to the URL.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        method, kwargs2 = handle_query_args(params)
        kwargs.update(kwargs2)

        return self.request(method, '_all_docs', **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_bulk_docs
    def bulk_docs(self, docs, json=None, **kwargs):
        """Create, update or delete multiple documents.

        :param list docs: Sequence of document objects to be sent.
        :param dict json: (optional) JSON to send in the body of the :class:`requests.Request`.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        kwargs['json'] = {} if not json else json
        kwargs['json'].update({'docs': docs})

        return self.request('POST', '_bulk_docs', **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact
    def compact(self, **kwargs):
        """Trigger a compaction operation.

        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        if 'json' not in kwargs:
            kwargs['json'] = {}  # Set application/json

        return self.request('POST', '_compact', **kwargs)

    # http://docs.couchdb.org/en/stable/api/ddoc/render.html#get--db-_design-ddoc-_list-func-view
    def ddoc_list(self, ddoc_id, func_id, view_id, other_id=None, **kwargs):
        """Apply a list function against a view.

        :param str ddoc_id: Design document name.
        :param str func_id: List function name.
        :param str view_id: View function name.
        :param str other_id: (optional) Other design document name that holds the view function.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        if other_id:
            path = join(encode_doc_id(other_id), view_id)
        else:
            path = view_id

        return self._ddoc('GET', ddoc_id, _LIST, func_id, path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/ddoc/render.html#get--db-_design-ddoc-_show-func
    def ddoc_show(self, ddoc_id, func_id, doc_id=None, **kwargs):
        """Apply a show function against a document.

        :param str ddoc_id: Design document name.
        :param str func_id: Show function name.
        :param str doc_id: (optional) Document ``_id`` to execute the show function on.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
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

        :param str ddoc_id: Design document name.
        :param str func_id: View function name.
        :param dict params: (optional) Parameters to append to the URL.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        method, kwargs2 = handle_query_args(params)
        kwargs.update(kwargs2)

        return self._ddoc(method, ddoc_id, _VIEW, func_id, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#delete--db
    def destroy(self, **kwargs):
        """Delete the database.

        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        # Don't try to setup the database
        return self.request('DELETE', _init=False, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
    def get(self, doc_id, params=None, **kwargs):
        """Retrieve a document.

        :param str doc_id: Document ``_id`` to retrieve.
        :param dict params: (optional) Parameters to append to the URL.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
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

        :param str doc_id: Document ``_id`` of attachment.
        :param str att_id: Attachment name to retrieve.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        path = join(encode_doc_id(doc_id), encode_att_id(att_id))
        return self.request('GET', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#get--db
    def info(self, **kwargs):
        """Get information about the database.

        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        return self.request('GET', **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
    # http://docs.couchdb.org/en/stable/api/database/common.html#post--db
    def insert(self, doc, **kwargs):
        """Create or update an existing document.

        :param dict doc: Document to insert.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        if '_id' in doc:
            method = 'PUT'
            path = encode_doc_id(doc['_id'])
        else:
            method = 'POST'
            path = ''

        kwargs['json'] = doc
        return self.request(method, path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/attachments.html#put--db-docid-attname
    def insert_att(self, doc_id, doc_rev, att_id, att, att_type, **kwargs):
        """Create or update an existing attachment.

        :param str doc_id: Document ``_id`` of attachment.
        :param str doc_rev: Document revision. (Can be ``None``)
        :param str att_id: Attachment name.
        :param att: Attachment dictionary, bytes, or file-like object to insert.
        :param str att_type: Attachment MIME type.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        if doc_rev:
            if 'params' not in kwargs:
                kwargs['params'] = {}
            kwargs['params']['rev'] = doc_rev
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        path = join(encode_doc_id(doc_id), encode_att_id(att_id))
        kwargs['headers']['Content-Type'] = att_type
        kwargs['data'] = att

        return self.request('PUT', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
    def remove(self, doc_id, doc_rev, **kwargs):
        """Delete a document.

        :param str doc_id: Document ``_id`` to remove.
        :param str doc_rev: Document revision.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
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

        :param str doc_id: Document ``_id`` of attachment.
        :param str doc_rev: Document revision.
        :param str att_id: Attachment name to remove.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        if 'params' not in kwargs:
            kwargs['params'] = {}

        path = join(encode_doc_id(doc_id), encode_att_id(att_id))
        kwargs['params']['rev'] = doc_rev

        return self.request('DELETE', path, **kwargs)

    # http://docs.couchdb.org/en/stable/api/server/common.html#replicate
    def replicate_to(self, target, json=None, **kwargs):
        """Replicate data from source (this) to target.

        :param str target: URL or name of the target database.
        :param dict json: (optional) JSON to send in the body of the :class:`requests.Request`.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        url = join(self.host, '_replicate')
        kwargs['json'] = {} if not json else json
        kwargs['json'].update({
            'source': self.url,
            'target': target,
        })

        return self.request('POST', url, _init=False, **kwargs)

    def request(self, method, path='', _init=True, **kwargs):
        """Construct a :class:`requests.Request` object and send it.

        :param str method: Method for the :class:`requests.Request` object.
        :param str path: (optional) Path to join with :attr:`CouchDB.url`.
        :param bool _init: (internal) Initialize the database.
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        # Check if the database exists
        if _init and self.create_db and (not self._created):
            try:
                self.request('HEAD', _init=False)
            except ResourceNotFound:
                # Or create it
                self.request('PUT', _init=False)
            self._created = True

        # Prepare the params dictionary
        if 'params' in kwargs and kwargs['params']:
            params = kwargs['params'].copy()
            for key, val in iteritems(params):
                # Handle Python booleans
                if type(val) == bool:
                    params[key] = dumps(val)
            kwargs['params'] = params

        if urlparse(path).scheme:
            url = path  # Handle absolute URLs
        else:
            url = join(self.url, path).strip('/')

        r = self.session.request(method, url, **kwargs)
        if not (200 <= r.status_code < 300):
            raise get_http_exception(r)

        return r

    def _ddoc(self, method, ddoc_id, func_type, func_id, _path=None, **kwargs):
        """Apply or execute a design document function.

        :param str method: Method for the :class:`requests.Request` object.
        :param str ddoc_id: Design document name.
        :param str func_type: Design function type.
        :param str func_id: Design function name.
        :param str _path: (optional) FIXME: What is this?
        :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
        :rtype: requests.Response
        """

        doc_id = join('_design', ddoc_id)
        path = join(encode_doc_id(doc_id), func_type, func_id)

        if _path:
            path = join(path, _path)

        return self.request(method, path, **kwargs)
