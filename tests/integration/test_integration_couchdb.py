# -*- coding: utf-8 -*-

import pytest

from time2relax import CouchDB, ResourceNotFound


def test_couchdb_create_database(db):
    db = CouchDB(db.url, create_database=False)

    with pytest.raises(ResourceNotFound) as ex:
        db.info()

    message = ex.value.args[1].json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'no_db_file'


def test_couchdb_setup(db):
    assert db._created is False
    db.info()
    assert db._created is True
