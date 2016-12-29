# -*- coding: utf-8 -*-

import pytest

from time2relax import CouchDB, ResourceNotFound


def test_couchdb(db):
    r = '<{0} [{1}]>'.format(db.__class__.__name__, db.url)

    assert isinstance(db, CouchDB)
    assert repr(db) == r

    assert db.host == 'http://localhost:5984'
    assert db.name == 'testdb'
    assert db.url == 'http://localhost:5984/testdb'
    assert db.skip_setup is False
    assert db.session.headers['Accept'] == 'application/json'


def test_couchdb_skip_setup(db):
    db = CouchDB(db.url, True)
    assert db.skip_setup is True

    with pytest.raises(ResourceNotFound) as ex:
        db.info()

    message = ex.value.response.json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'no_db_file'


def test_couchdb_has_setup(db):
    assert db._has_setup is False
    db.info()
    assert db._has_setup is True
