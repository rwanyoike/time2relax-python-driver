# -*- coding: utf-8 -*-


def test_insert_att(db):
    r = db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    result = r.json()
    assert 'ok' in result


def test_insert_att_update(db):
    r = db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    result = r.json()

    db.insert_att(result['id'], result['rev'], 'att.txt', 'v9mZ', 'text/raw')
    r = db.get_att('doc', 'att.txt')

    assert r.headers['Content-Type'] == 'text/raw'
    assert r.text == 'v9mZ'


def test_insert_att_params(db):
    r = db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain',
                      params={'x-assert': True})
    assert 'x-assert' in r.request.url


def test_insert_att_kwargs(db):
    r = db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    result = r.json()

    r = db.insert_att('doc', result['rev'], 'att.txt', 'v9mZ', 'text/raw',
                      params={}, headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
