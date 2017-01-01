# -*- coding: utf-8 -*-


def test_info(db):
    db.insert({'_id': 'someid'})
    r = db.info()
    result = r.json()

    assert result['doc_count'] == 1
    assert result['doc_del_count'] == 0


def test_info_kwargs(db):
    r = db.info(headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
