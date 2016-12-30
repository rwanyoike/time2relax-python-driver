# -*- coding: utf-8 -*-

import pytest

from time2relax import CouchDB, ResourceNotFound


def test_couchdb_skip_setup(db):
    db = CouchDB(db.url, skip_setup=True)

    with pytest.raises(ResourceNotFound) as ex:
        db.info()

    message = ex.value.response.json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'no_db_file'


def test_couchdb_setup(db):
    assert db._setup is False
    db.info()
    assert db._setup is True
