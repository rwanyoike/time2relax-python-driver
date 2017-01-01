# -*- coding: utf-8 -*-


def test_request(db):
    params = {'a': True, 'b': False, 'c': 'cat'}
    r = db.request('HEAD', db.url, params=params)

    assert 'a=true' in r.request.url
    assert 'b=false' in r.request.url
    assert 'c=cat' in r.request.url
