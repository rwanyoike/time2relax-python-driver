# -*- coding: utf-8 -*-


def test_info(db):
    db.insert({'_id': 'someid'})
    response = db.info()
    result = response.json()

    assert result['doc_count'] == 1
    assert result['doc_del_count'] == 0


def test_info_kwargs(db):
    response = db.info(headers={'X-Assert': 'true'})
    assert 'X-Assert' in response.request.headers
