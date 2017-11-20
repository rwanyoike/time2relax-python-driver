# -*- coding: utf-8 -*-

import time


def test_compact(db):
    db.insert({'_id': 'someid'})
    r = db.compact()
    time.sleep(2)  # wait for compact
    assert 'ok' in r.json()


def test_compact_kwargs(db):
    r = db.compact(json={}, headers={'X-Assert': 'true'})
    time.sleep(2)  # wait for compact
    assert 'X-Assert' in r.request.headers
