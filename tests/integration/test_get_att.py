# -*- coding: utf-8 -*-


def test_get_att(db):
    db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    response = db.get_att('doc', 'att.txt')

    assert response.headers['Content-Type'] == 'text/plain'
    assert response.text == 'Zm9v'


def test_get_att_kwargs(db):
    db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    response = db.get_att('doc', 'att.txt', headers={'X-Assert': 'true'})

    assert 'X-Assert' in response.request.headers
