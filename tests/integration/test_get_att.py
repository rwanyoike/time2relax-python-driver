# -*- coding: utf-8 -*-


def test_get_att(db):
    db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    response = db.get_att('doc', 'att')

    assert response.headers['Content-Type'] == 'text/plain'
    assert response.text == 'Zm9v'


def test_get_att_kwargs(db):
    db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    response = db.get_att('doc', 'att', headers={'X-Assert': 'true'})

    assert 'X-Assert' in response.request.headers
