# -*- coding: utf-8 -*-


def test_insert_post(db):
    r = db.insert({'test': 'somestuff'})
    result = r.json()

    assert r.request.method == 'POST'
    assert 'ok' in result


def test_insert_put(db):
    r = db.insert({'_id': 'someid'})
    result = r.json()

    assert r.request.method == 'PUT'
    assert 'ok' in result


def test_insert_kwargs(db):
    r = db.insert({}, headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
