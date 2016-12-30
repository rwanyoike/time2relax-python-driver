# -*- coding: utf-8 -*-


def test_request(db):
    params = {'a': True, 'b': False, 'c': 'cat'}
    response = db.request('HEAD', db.url, params=params)

    assert 'a=true' in response.request.url
    assert 'b=false' in response.request.url
    assert 'c=cat' in response.request.url
