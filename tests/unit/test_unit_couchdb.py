# -*- coding: utf-8 -*-

from time2relax import CouchDB


def test_couchdb(db):
    r = '<{0} [{1}]>'.format(db.__class__.__name__, db.url)

    assert isinstance(db, CouchDB)
    assert repr(db) == r
    assert db.session.headers['Accept'] == 'application/json'
