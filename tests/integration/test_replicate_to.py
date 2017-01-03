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
    db2.destroy()

    result = r.json()
    assert result['doc_count'] == 3


def test_replicate_to_kwargs(db):
    db.request('HEAD')  # setup db
    db2 = CouchDB(db.host + '/dbtest')
    db2.request('HEAD')  # setup db

    r = db.replicate_to(db2.url, json={}, headers={'X-Assert': 'true'})
    db2.destroy()

    assert 'X-Assert' in r.request.headers
