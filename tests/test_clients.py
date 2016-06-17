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
    j, h = client.request('GET', url)

    assert j == data
    assert h == {'Content-Type': 'application/json'}


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
        999: CouchDbError,
    }

    client = HTTPClient()
    url = 'http://example.com'
    data = {'py.test': 100}

    for i in exceptions:
        with RequestsMock() as rm, pytest.raises(exceptions[i]):
            rm.add('GET', url, json=data, status=i)
            client.request('GET', url)
