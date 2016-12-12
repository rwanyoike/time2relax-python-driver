# -*- coding: utf-8 -*-

import pytest
import responses
from requests.models import Response
from responses import RequestsMock

from time2relax import HTTPClient, Server, Database, CouchDbError, \
    BadRequest, Unauthorized, Forbidden, ResourceNotFound, MethodNotAllowed, \
    ResourceConflict, PreconditionFailed, ServerError


@responses.activate
def test_client_request():
    """Tests. Tests. Tests."""

    url = 'http://example.com'
    data = {'py.test': 100}
    responses.add('GET', url, json=data, status=200)
    r = HTTPClient().request('GET', url)

    assert r.headers == {'Content-Type': 'application/json'}
    assert r.json() == data


def test_client_errors():
    """Tests. Tests. Tests."""

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

    client = HTTPClient()
    url = 'http://example.com'
    data = {'py.test': 100}
    rm = RequestsMock()
    rm.start()

    for i in exceptions:
        rm.add('GET', url, json=data, status=i)
        with pytest.raises(exceptions[i]):
            client.request('GET', url)

    rm.add('HEAD', url, status=999)
    with pytest.raises(CouchDbError):
        client.request('HEAD', url)

    rm.stop()
    rm.reset()


def test_server_object():
    """Tests. Tests. Tests."""

    server = Server()
    r = '<{0} [{1}]>'.format(server.__class__.__name__, server.url)

    assert repr(server) == r


def test_database_object():
    """Tests. Tests. Tests."""

    database = Database(Server(), 'test')
    r = '<{0} [{1}]>'.format(database.__class__.__name__, database.name)

    assert repr(database) == r


def test_error_object():
    """Tests. Tests. Tests."""

    message = {'error': 'time2relax', 'reason': 'CouchDB'}
    res = Response()
    with pytest.raises(CouchDbError) as ex:
        raise CouchDbError(message, res)

    assert ex.value.response == res
