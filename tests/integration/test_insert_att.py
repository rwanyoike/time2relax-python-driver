# -*- coding: utf-8 -*-


def test_insert_att(db):
    response = db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    result = response.json()

    assert 'ok' in result


def test_insert_att_update(db):
    response = db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    result = response.json()

    db.insert_att(result['id'], 'att', result['rev'], 'v9mZ', 'text/raw')
    response = db.get_att('doc', 'att')

    assert response.headers['Content-Type'] == 'text/raw'
    assert response.text == 'v9mZ'


def test_insert_att_params(db):
    response = db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain',
                             params={'x-assert': True})
    assert 'x-assert' in response.request.url


def test_insert_att_kwargs(db):
    response = db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    result = response.json()

    response = db.insert_att('doc', 'att', result['rev'], 'v9mZ', 'text/raw',
                             params={}, headers={'X-Assert': 'true'})

    assert 'X-Assert' in response.request.headers
