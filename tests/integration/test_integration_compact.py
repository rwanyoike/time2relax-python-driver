# -*- coding: utf-8 -*-

import time


def test_compact(db):
    db.insert({'_id': 'someid'})
    r = db.compact()
    time.sleep(2)  # wait

    result = r.json()
    assert 'ok' in result


def test_compact_kwargs(db):
    r = db.compact(json={}, headers={'X-Assert': 'true'})
    time.sleep(2)  # wait

    assert 'X-Assert' in r.request.headers
