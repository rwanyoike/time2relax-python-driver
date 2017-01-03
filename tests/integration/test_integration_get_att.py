# -*- coding: utf-8 -*-


def test_get_att(db):
    db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')

    r = db.get_att('doc', 'att.txt')
    assert r.headers['Content-Type'] == 'text/plain'
    assert r.text == 'Zm9v'


def test_get_att_kwargs(db):
    db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')

    r = db.get_att('doc', 'att.txt', headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
