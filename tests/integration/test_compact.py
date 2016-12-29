# -*- coding: utf-8 -*-


def test_compact(db):
    db.insert({'_id': 'someid'})
    response = db.compact()
    result = response.json()

    assert 'ok' in result


def test_compact_kwargs(db):
    response = db.compact(json={}, headers={'X-Assert': 'true'})

    assert 'X-Assert' in response.request.headers
