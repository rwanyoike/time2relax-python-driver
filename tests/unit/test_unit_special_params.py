# -*- coding: utf-8 -*-


def test_special_params(db):
    params = {'start_key': ['x'], 'endkey': 2}
    method, meta = db._special_params(params)

    assert method == 'GET'
    assert meta['params'] == {'endkey': '2', 'start_key': '["x"]'}


def test_special_params_post(db):
    params = {'keys': [2, '10', True, 'abcd']}
    method, meta = db._special_params(params)

    assert method == 'POST'
    assert meta['json']['keys'] == [2, '10', True, 'abcd']
    assert meta['params'] == {}
