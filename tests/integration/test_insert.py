# -*- coding: utf-8 -*-


def test_insert_post(db):
    response = db.insert({'test': 'somestuff'})
    result = response.json()

    assert response.request.method == 'POST'
    assert 'ok' in result


def test_insert_put(db):
    response = db.insert({'_id': 'someid'})
    result = response.json()

    assert response.request.method == 'PUT'
    assert 'ok' in result


def test_insert_kwargs(db):
    response = db.insert({}, headers={'X-Assert': 'true'})
    assert 'X-Assert' in response.request.headers
