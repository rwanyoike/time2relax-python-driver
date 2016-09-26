# -*- coding: utf-8 -*-

import pytest
import responses
from responses import RequestsMock

from time2relax.clients import HTTPClient
from time2relax.errors import (BadRequest, ResourceConflict, CouchDbError,
                               MethodNotAllowed, ServerError, ResourceNotFound,
                               Unauthorized, Forbidden, PreconditionFailed)


@responses.activate
def test_http_client_request():
    """Tests. Tests. Tests."""

    client = HTTPClient()
    url = 'http://example.com'
    data = {'py.test': 100}

    responses.add('GET', url, json=data, status=200)
    r = client.request('GET', url)

    assert r.headers == {'Content-Type': 'application/json'}
    assert r.json() == data


def test_http_client_errors():
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
