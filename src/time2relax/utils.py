"""Utility methods that are used in time2relax."""

import functools
import json
from posixpath import join as urljoin

from requests import compat

from time2relax import exceptions

HTTP_EXCEPTIONS = {
    400: exceptions.BadRequest,
    401: exceptions.Unauthorized,
    403: exceptions.Forbidden,
    404: exceptions.ResourceNotFound,
    405: exceptions.MethodNotAllowed,
    409: exceptions.ResourceConflict,
    412: exceptions.PreconditionFailed,
    500: exceptions.ServerError,
}

JSON_QUERY_ARGS = (
    "end_key",
    "endkey",
    "key",
    "start_key",
    "startkey",
)


def encode_uri_component(part: str) -> str:
    """Return an encoded URI component.

    https://stackoverflow.com/a/6618858

    Example::

        >>> encode_uri_component('escaped%2F1')
        'escaped%252F1'

    :param str part: The URI component.
    :rtype: str
    """
    return compat.quote(part, "~()*!.'")


def encode_attachment_id(_id):
    """Return an encoded attachment id.

    Example::

        >>> encode_attachment_id('a0+$/9_()')
        'a0%2B%24/9_()'

    :param str _id: The attachment id.
    :rtype: str
    """
    paths = map(encode_uri_component, _id.split("/"))
    return urljoin(*paths)


def encode_document_id(_id):
    """Return an encoded document id.

    Example::

        >>> encode_document_id('foo+bar')
        'foo%2Bbar'

    :param str _id: The document id.
    :rtype: str
    """
    if _id.startswith("_design"):
        uri = encode_uri_component(_id[8:])
        return f"_design/{uri}"

    if _id.startswith("_local"):
        uri = encode_uri_component(_id[7:])
        return f"_local/{uri}"

    return encode_uri_component(_id)


def get_database_host(url):
    """Return a database host in a URL.

    Example::

        >>> get_database_host('http://foobar.com:5984/testdb')
        'http://foobar.com:5984'

    :param str url: The URL to parse.
    :rtype: str
    """
    components = compat.urlparse(url)[:2] + (("",) * 4)
    return compat.urlunparse(components)


def get_database_name(url):
    """Return a database name in a URL.

    Example::

        >>> get_database_name('http://foobar.com:5984/testdb')
        'testdb'

    :param str url: The URL to parse.
    :rtype: str
    """
    name = compat.urlparse(url).path.strip("/").split("/")[-1]

    # Avoid re-encoding the name
    if "%" not in name:
        name = encode_uri_component(name)

    return name


def query_method_kwargs(params):
    """Return a method and kwargs to handle a query.

    http://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options

    Example::

        >>> params = {'start_key': ['x'], 'endkey': 2}
        >>> query_method_kwargs(params)
        ('GET', {'params': {'start_key': '["x"]', 'endkey': '2'}})

    :param dict params: The URL parameters.
    :rtype: (str, dict)
    """
    method = "GET"
    kwargs = {}

    if params:
        _params = dict(params)

        # If 'keys' is supplied, issue a POST request to circumvent GET query limits
        if "keys" in _params:
            method = "POST"
            kwargs["json"] = {"keys": _params["keys"]}
            del _params["keys"]

        # These arguments to be properly JSON encoded values
        for i in JSON_QUERY_ARGS:
            if i in _params:
                _params[i] = json.dumps(_params[i])
        if _params:
            kwargs["params"] = _params

    return method, kwargs


def raise_http_exception(response):
    """Raise a HTTP exception.

    http://docs.couchdb.org/en/stable/api/basics.html#http-status-codes

    :param requests.Response response: The response object.
    :rtype: exceptions.HTTPError
    """
    try:
        message = response.json()
    except ValueError:
        message = None

    ex = HTTP_EXCEPTIONS.get(response.status_code, exceptions.HTTPError)

    raise ex(message, response)


def relax(f):
    """Execute a time2relax model function.

    :param function f: The function to call.
    :rtype: function
    """

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            # Hack-y alternative to copy-pasting
            m, p, k = f(*args[1:], **kwargs)
            c = args[0]
            return c.request(m, p, **k)

        return inner

    return decorator
