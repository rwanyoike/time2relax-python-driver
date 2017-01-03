# -*- coding: utf-8 -*-

import pytest
from responses import RequestsMock

import time2relax
from time2relax import CouchDB


def test_request(db):
    params = {'a': True, 'b': False, 'c': 'cat'}
    r = db.request('HEAD', params=params)

    assert 'a=true' in r.request.url
    assert 'b=false' in r.request.url
    assert 'c=cat' in r.request.url


def test_request_exceptions(db):
    db = CouchDB(db.url, True)

    exceptions = {
        400: time2relax.BadRequest,
        401: time2relax.Unauthorized,
        403: time2relax.Forbidden,
        404: time2relax.ResourceNotFound,
        405: time2relax.MethodNotAllowed,
        409: time2relax.ResourceConflict,
        412: time2relax.PreconditionFailed,
        500: time2relax.ServerError,
        999: time2relax.CouchDBError,
    }

    rm = RequestsMock()
    rm.start()

    for i in exceptions:
        rm.add('GET', db.url, status=i)
        with pytest.raises(exceptions[i]):
            db._request('GET', db.url)

    rm.stop()
    rm.reset()
