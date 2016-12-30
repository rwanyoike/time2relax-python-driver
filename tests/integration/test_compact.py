# -*- coding: utf-8 -*-

import time


def test_compact(db):
    db.insert({'_id': 'someid'})
    response = db.compact()
    time.sleep(2)
    result = response.json()

    assert 'ok' in result


def test_compact_kwargs(db):
    response = db.compact(json={}, headers={'X-Assert': 'true'})
    time.sleep(2)

    assert 'X-Assert' in response.request.headers
