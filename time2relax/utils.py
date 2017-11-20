# -*- coding: utf-8 -*-

"""
time2relax.utils
~~~~~~~~~~~~~~~~

This module provides utility functions that are used within time2relax that are
also useful for external consumption.
"""

from json import dumps
from posixpath import join as urljoin

from requests.compat import quote, urlparse, urlunparse

from .exceptions import (
    BadRequest, Forbidden, HTTPError, MethodNotAllowed, PreconditionFailed, ResourceConflict,
    ResourceNotFound, ServerError, Unauthorized)

# http://docs.couchdb.org/en/stable/api/basics.html?#http-status-codes
EXCEPTIONS = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: ResourceNotFound,
    405: MethodNotAllowed,
    409: ResourceConflict,
    412: PreconditionFailed,
    500: ServerError,
}

# http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
QUERY_ARGS = ('start_key', 'startkey', 'end_key', 'endkey', 'key')


def encode_uri_component(component):
    """Encode a uri component:

    >>> encode_uri_component('escaped%2F1')
    'escaped%252F1'

    :param component: The URI component.
    :rtype: str
    """

    # http://stackoverflow.com/a/6618858/2497865
    return quote(component, "~()*!.\'")


def encode_att_id(_id):
    """Encode an attachment id:

    >>> encode_att_id('a0+$/9_()')
    'a0%2B%24/9_()'

    :param _id: The attachment id.
    :rtype: str
    """

    return urljoin(*map(encode_uri_component, _id.split('/')))


def encode_doc_id(_id):
    """Encode a document id:

    >>> encode_doc_id('some+id')
    'some%2Bid'

    :param _id: The document id.
    :rtype: str
    """

    if _id.startswith('_design'):
        uri = encode_uri_component(_id[8:])
        return '_design/{0}'.format(uri)

    if _id.startswith('_local'):
        uri = encode_uri_component(_id[7:])
        return '_local/{0}'.format(uri)

    return encode_uri_component(_id)


def get_database_host(url):
    """Get the database host from a URL:

    >>> get_database_host('http://foobar.com:5984/testdb')
    'http://foobar.com:5984'

    :param url: The URL to parse.
    :rtype: str
    """

    return urlunparse(urlparse(url)[:2] + ('',) * 4)


def get_database_name(url):
    """Get the database name from a URL:

    >>> get_database_name('http://foobar.com:5984/testdb')
    'testdb'

    :param url: The URL to parse.
    :rtype: str
    """

    name = urlparse(url).path \
        .strip('/') \
        .split('/').pop()

    # Avoid re-encoding
    if '%' not in name:
        name = encode_uri_component(name)

    return name


def handle_query_args(params):
    """Handle special CouchDB query arguments:

    >>> params = {'start_key': ['x'], 'endkey': 2}
    >>> handle_query_args(params)
    ('GET', {'params': {'start_key': '["x"]', 'endkey': '2'}})

    :param params: Dictionary of URL parameters.
    :rtype: str, dict
    """

    method = 'GET'
    kwargs = {}

    if params:
        params = params.copy()

        if 'keys' in params:
            # If `keys` are supplied, issue a POST to circumvent GET query
            # string limits.
            method = 'POST'
            kwargs['json'] = {'keys': params['keys']}  # replace
            params.pop('keys', None)

        for i in QUERY_ARGS:
            if i in params:
                params[i] = dumps(params[i])

        kwargs['params'] = params

    return method, kwargs


def get_http_exception(r):
    """
    :param requests.Response r:
    :rtype: HTTPError
    """

    try:
        message = r.json()
    except ValueError:
        message = None

    if r.status_code in EXCEPTIONS:
        ex = EXCEPTIONS[r.status_code]
    else:
        # Worst-case
        ex = HTTPError

    return ex(message, r)
