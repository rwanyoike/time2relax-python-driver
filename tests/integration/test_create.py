# -*- coding: utf-8 -*-

from conftest import COUCHDB_URL
from time2relax import CouchDB


def test_create(db):
    r = db.info()
    result = r.json()
    assert result['db_name'] == db.name


def test_create_complex():
    db_name = 'az09_$()+-'
    result = _put_db_name(db_name)
    assert result['db_name'] == db_name


def test_create_slash():
    result = _put_db_name('with/slash')
    assert result['db_name'] == 'slash'


def test_create_escaped():
    result = _put_db_name('escaped%2F1')
    assert result['db_name'] == 'escaped/1'


def _put_db_name(db_name):
    db = CouchDB(COUCHDB_URL + db_name)
    r = db.info()
    db.destroy()

    return r.json()
