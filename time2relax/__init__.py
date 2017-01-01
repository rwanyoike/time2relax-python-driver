# -*- coding: utf-8 -*-

#             __
# _|_ o __  _  _) __ _  |  _
#  |_ | |||(/_/__ | (/_ | (_|><
#

from json import dumps
from posixpath import join as urljoin

from requests import Session
from requests.compat import quote, urlparse, urlunparse
from six import iteritems

__version__ = '0.3.0'

_LIST = '_list'
_SHOW = '_show'
_VIEW = '_view'


class CouchDB(object):
    """Representation of a CouchDB database."""

    _destroyed = False
    _setup = False

    def __init__(self, url, skip_setup=False):
        """Initialize the database object.

        :param url: Database url to use.
        :param skip_setup: Don't setup the database.
        """

        self.host = self._get_db_host(url)
        self.name = self._get_db_name(url)
        self.url = urljoin(self.host, self.name)
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
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        url = self._get_db_url('_all_docs')
        meta = self._special_params(params)
        method = meta.pop('method')

        kwargs.update(meta)

        return self.request(method, url, **kwargs)

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

        url = self._get_db_url('_bulk_docs')

        if not json:
            json = {}
        json.update({'docs': docs})

        kwargs['json'] = json

        return self.request('POST', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact
    def compact(self, **kwargs):
        """Trigger a compaction operation.

        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        url = self._get_db_url('_compact')

        if 'json' not in kwargs:
            kwargs['json'] = {}  # application/json

        return self.request('POST', url, **kwargs)

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
            path = urljoin(self._encode_doc_id(other_id), view_id)
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
            path = self._encode_doc_id(doc_id)
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

        meta = self._special_params(params)
        method = meta.pop('method')

        kwargs.update(meta)

        return self._ddoc(method, ddoc_id, _VIEW, func_id, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#delete--db
    def destroy(self, **kwargs):
        """Delete the database.

        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        # Don't setup the database
        response = self.request('DELETE', self.url, True, **kwargs)
        # Prevent further requests
        self._destroyed = True

        return response

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
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        path = urljoin(self._encode_doc_id(doc_id),
                       self._encode_att_id(att_id))
        url = self._get_db_url(path)

        return self.request('GET', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/database/common.html#get--db
    def info(self, **kwargs):
        """Get information about the database.

        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        return self.request('GET', self.url, **kwargs)

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
            url = self._get_db_url(self._encode_doc_id(doc['_id']))
        else:
            method = 'POST'
            url = self.url

        kwargs['json'] = doc  # hijack

        return self.request(method, url, **kwargs)

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

        path = urljoin(self._encode_doc_id(doc_id),
                       self._encode_att_id(att_id))
        url = self._get_db_url(path)

        if doc_rev:
            if 'params' not in kwargs:
                kwargs['params'] = {}
            kwargs['params']['rev'] = doc_rev

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Content-Type'] = att_type
        kwargs['data'] = att  # hijack

        return self.request('PUT', url, **kwargs)

    # http://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
    def remove(self, doc_id, doc_rev, **kwargs):
        """Delete a document.

        :param doc_id: Document ``_id`` to remove.
        :param doc_rev: Document revision.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        url = self._get_db_url(self._encode_doc_id(doc_id))

        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['rev'] = doc_rev

        return self.request('DELETE', url, **kwargs)

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

        path = urljoin(self._encode_doc_id(doc_id),
                       self._encode_att_id(att_id))
        url = self._get_db_url(path)

        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['rev'] = doc_rev

        return self.request('DELETE', url, **kwargs)

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

        if json is None:
            json = {}
        json.update({
            'source': self.url,
            'target': target,
        })

        kwargs['json'] = json

        return self.request('POST', url, **kwargs)

    def request(self, method, url, skip_setup=False, **kwargs):
        """Construct a :class:`requests.Request` object and send it.

        :param method: Method for the new :class:`requests.Request` object.
        :param url: URL for the new :class:`requests.Request` object.
        :param skip_setup: Don't setup the database.
        :param kwargs: (optional) Arguments that :class:`requests.Request`
            takes.
        :rtype: requests.Response
        """

        if self._destroyed:
            raise CouchDBError('Database is destroyed :(')

        if not skip_setup and not self.skip_setup:
            if not self._setup:
                self._setup_database()

        if 'params' in kwargs and kwargs['params']:
            params = self._prepare_params(kwargs['params'])
            kwargs['params'] = params

        return self._request(method, url, **kwargs)

    @staticmethod
    def _check_response(response):
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
        path = urljoin(self._encode_doc_id(doc_id), func_type, func_id)

        if extra:
            path = urljoin(path, extra)

        url = self._get_db_url(path)

        return self.request(method, url, **kwargs)

    @staticmethod
    def _encode_att_id(att_id):
        """Encode an attachment id."""

        parts = map(CouchDB._encode_uri_component, att_id.split('/'))
        return urljoin(*parts)

    @staticmethod
    def _encode_doc_id(doc_id):
        """Encode a document id."""

        if doc_id.startswith('_design'):
            uri = CouchDB._encode_uri_component(doc_id[8:])
            return '_design/{0}'.format(uri)

        if doc_id.startswith('_local'):
            uri = CouchDB._encode_uri_component(doc_id[7:])
            return '_local/{0}'.format(uri)

        return CouchDB._encode_uri_component(doc_id)

    @staticmethod
    def _encode_uri_component(component):
        """Encode a uri component."""

        # http://stackoverflow.com/a/6618858/2497865
        return quote(component, "~()*!.\'")

    @staticmethod
    def _get_db_host(url):
        """Get the database host from a url."""

        uri = urlparse(url)
        # http://stackoverflow.com/a/9627834/2497865
        return urlunparse(uri[:2] + ('',) * 4)

    @staticmethod
    def _get_db_name(url):
        """Get the database name from a url."""

        uri = urlparse(url)
        name = uri.path.strip('/').split('/').pop()

        # Prevent double encoding
        if '%' not in name:
            name = CouchDB._encode_uri_component(name)

        return name

    def _get_db_url(self, path):
        """Build a database url from a path."""

        return urljoin(self.url, path)

    @staticmethod
    def _prepare_params(params):
        """Prepare a ``params`` dictionary."""

        params = params.copy()  # mutable!

        for key, val in iteritems(params):
            # Handle Python titlecase booleans
            if type(val) == bool:
                params[key] = dumps(val)

        return params

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

        self._setup = True

    @staticmethod
    def _special_params(params):
        """Handle special CouchDB query arguments."""

        meta = {'method': 'GET'}

        if params:
            params = params.copy()  # mutable!

            # If `keys` are supplied, issue a POST to circumvent GET query
            # string limits.
            # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
            if 'keys' in params:
                meta['method'] = 'POST'
                meta['json'] = {'keys': params['keys']}
                params.pop('keys', None)

            # http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
            for i in ('start_key', 'startkey', 'end_key', 'endkey', 'key'):
                if i in params:
                    params[i] = dumps(params[i])

            meta['params'] = params

        return meta


class CouchDBError(Exception):
    """Class for errors based on bad HTTP status codes."""

    # http://docs.couchdb.org/en/stable/api/basics.html?#http-status-codes
    def __init__(self, message, response=None):
        """Initialize the exception object.

        :param message: Exception message.
        :param response: ``response`` object.
        """

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
