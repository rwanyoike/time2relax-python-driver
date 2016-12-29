# -*- coding: utf-8 -*-

import pytest
from responses import RequestsMock

import time2relax
from time2relax import CouchDB, BadRequest, Unauthorized, Forbidden, \
    ResourceNotFound, MethodNotAllowed, ResourceConflict, PreconditionFailed, \
    ServerError, CouchDBError


def test_time2relax():
    assert time2relax.__version__


def test_time2relax_exceptions(db):
    db = CouchDB(db.url, True)

    exceptions = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: ResourceNotFound,
        405: MethodNotAllowed,
        409: ResourceConflict,
        412: PreconditionFailed,
        500: ServerError,
        999: CouchDBError,
    }

    rm = RequestsMock()
    rm.start()

    for i in exceptions:
        rm.add('GET', db.url, status=i)
        with pytest.raises(exceptions[i]):
            db.request('GET', db.url)

    rm.stop()
    rm.reset()
