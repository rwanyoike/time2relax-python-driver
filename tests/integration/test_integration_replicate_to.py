# -*- coding: utf-8 -*-

from time2relax import CouchDB


def test_replicate_to(db):
    db.insert({'test': 'somestuff'})
    db.insert({'test': 'somestuff'})
    db.insert({'test': 'somestuff'})
    db2 = CouchDB(db.host + '/dbtest')
    db2.request('HEAD')  # setup db

    db.replicate_to(db2.url)
    r = db2.info()
    db2.destroy()  # destroy db

    assert r.json()['doc_count'] == 3


def test_replicate_to_kwargs(db):
    db.insert({'test': 'somestuff'})
    db2 = CouchDB(db.host + '/dbtest')
    db2.request('HEAD')  # setup db

    r = db.replicate_to(db2.url, headers={'X-Assert': 'true'})
    db2.destroy()  # destroy db

    assert 'X-Assert' in r.request.headers
