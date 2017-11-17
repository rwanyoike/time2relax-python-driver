# -*- coding: utf-8 -*-

import pytest
from responses import RequestsMock

from time2relax import (
    CouchDB, BadRequest, Unauthorized, Forbidden, ResourceNotFound,
    MethodNotAllowed, ResourceConflict, PreconditionFailed, ServerError,
    CouchDBError)


def test_CouchDB_repr(database_url):
    db = CouchDB(database_url)
    r = '<{0} [{1}]>'.format(db.__class__.__name__, db.url)
    assert repr(db) == r


def test_CouchDB_session(database_url):
    db = CouchDB(database_url)
    assert db.session.headers['Accept'] == 'application/json'


def test_CouchDB_request(database_url):
    db = CouchDB(database_url, True)
    errors = {
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

    with RequestsMock() as rm:
        # BUG: If rm.add() and db._request() are in the same loop
        for i in errors:
            rm.add('GET', db.url, status=i)
        for i in errors:
            with pytest.raises(errors[i]):
                db._request('GET', db.url)
