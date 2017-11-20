# -*- coding: utf-8 -*-

import pytest
from responses import RequestsMock

from time2relax import (
    CouchDB, BadRequest, Forbidden, HTTPError, MethodNotAllowed, PreconditionFailed,
    ResourceConflict, ResourceNotFound, ServerError, Unauthorized)


def test_couchdb_session(database_url):
    db = CouchDB(database_url)
    assert db.session.headers['Accept'] == 'application/json'


def test_couchdb_repr(database_url):
    db = CouchDB(database_url)
    r = '<{0} [{1}]>'.format(db.__class__.__name__, db.url)
    assert repr(db) == r


def test_couchdb_request(database_url):
    db = CouchDB(database_url, True)
    exceptions = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: ResourceNotFound,
        405: MethodNotAllowed,
        409: ResourceConflict,
        412: PreconditionFailed,
        500: ServerError,
        999: HTTPError,
    }

    with RequestsMock() as rm:
        # BUG: If rm.add() and db.request() are in the same loop
        for i in exceptions:
            rm.add('GET', db.url, status=i)
        for i in exceptions:
            with pytest.raises(exceptions[i]):
                db.request('GET', _init=False)
