# -*- coding: utf-8 -*-

from requests import Response

from time2relax import (
    BadRequest, Forbidden, HTTPError, MethodNotAllowed, PreconditionFailed, ResourceConflict,
    ResourceNotFound, ServerError, Unauthorized)
from time2relax.utils import (
    encode_att_id, encode_doc_id, encode_uri_component, get_db_host, get_db_name,
    get_http_exception, handle_query_args)


def test_encode_att_id():
    r1 = encode_att_id('d/e/f.txt')
    assert r1 == 'd/e/f.txt'

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


def test_encode_uri_component():
    r1 = encode_uri_component('escaped%2F1')
    assert r1 == 'escaped%252F1'

    r2 = encode_uri_component('a/b/c')
    assert r2 == 'a%2Fb%2Fc'

    r3 = encode_uri_component('az09_$()+-')
    assert r3 == 'az09_%24()%2B-'


def test_get_db_host():
    r1 = get_db_host('http://foobar.com:5984/testdb')
    assert r1 == 'http://foobar.com:5984'

    r2 = get_db_host('http://u:p@foo.com/a/b/index.html?hey=yo')
    assert r2 == 'http://u:p@foo.com'


def test_get_db_name():
    r1 = get_db_name('http://foobar.com:5984/testdb')
    assert r1 == 'testdb'

    r2 = get_db_name('http://u:p@foo.com/a/b/index.html?hey=yo')
    assert r2 == 'index.html'


def test_get_http_exception():
    exceptions = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: ResourceNotFound,
        405: MethodNotAllowed,
        409: ResourceConflict,
        412: PreconditionFailed,
        500: ServerError,
        999: HTTPError,
    }

    for i in exceptions:
        r = Response()
        r.status_code = i
        assert isinstance(get_http_exception(r), exceptions[i])


def test_handle_query_args():
    m1, k1 = handle_query_args({'start_key': ['x'], 'endkey': 2})
    assert m1 == 'GET'
    assert k1['params'] == {'endkey': '2', 'start_key': '["x"]'}

    m2, k2 = handle_query_args({'keys': [2, '10', True, 'abcd']})
    assert m2 == 'POST'
    assert k2['json']['keys'] == [2, '10', True, 'abcd']
    assert k2['params'] == {}
