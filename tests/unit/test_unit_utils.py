# -*- coding: utf-8 -*-

from time2relax.utils import (
    encode_uri_component, encode_att_id, encode_doc_id, get_database_host,
    get_database_name, handle_query_args)


def test_encode_uri_component():
    r1 = encode_uri_component('escaped%2F1')
    assert r1 == 'escaped%252F1'

    # URI with /'s
    r2 = encode_uri_component('a/b/c')
    assert r2 == 'a%2Fb%2Fc'

    # Complex URI
    r3 = encode_uri_component('az09_$()+-')
    assert r3 == 'az09_%24()%2B-'


def test_encode_att_id():
    r1 = encode_att_id('d/e/f.txt')
    assert r1 == 'd/e/f.txt'

    # Complex id
    r2 = encode_att_id('a0+$/9_()')
    assert r2 == 'a0%2B%24/9_()'


def test_encode_doc_id():
    r1 = encode_doc_id('some+id')
    assert r1 == 'some%2Bid'

    # _design id
    r2 = encode_doc_id('_design/a/b/c')
    assert r2 == '_design/a%2Fb%2Fc'

    # _local id
    r3 = encode_doc_id('_local/az09_$()+-')
    assert r3 == '_local/az09_%24()%2B-'


def test_get_database_host():
    r1 = get_database_host('http://foobar.com:5984/testdb')
    assert r1 == 'http://foobar.com:5984'

    # Complex url
    r2 = get_database_host('http://user:pass@foo.com/a/b/index.html?hey=yo')
    assert r2 == 'http://user:pass@foo.com'


def test_get_database_name():
    r1 = get_database_name('http://foobar.com:5984/testdb')
    assert r1 == 'testdb'

    # Complex url
    r2 = get_database_name('http://user:pass@foo.com/a/b/index.html?hey=yo')
    assert r2 == 'index.html'


def test_handle_query_args():
    m1, k1 = handle_query_args({'start_key': ['x'], 'endkey': 2})
    assert m1 == 'GET'
    assert k1['params'] == {'endkey': '2', 'start_key': '["x"]'}

    # POST method
    m2, k2 = handle_query_args({'keys': [2, '10', True, 'abcd']})
    assert m2 == 'POST'
    assert k2['json']['keys'] == [2, '10', True, 'abcd']
    assert k2['params'] == {}
