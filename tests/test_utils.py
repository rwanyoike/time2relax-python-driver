import pytest

from time2relax import exceptions, utils


def test_encode_uri_component():
    assert utils.encode_uri_component('escaped%2F1') == 'escaped%252F1'
    assert utils.encode_uri_component('a/b/c') == 'a%2Fb%2Fc'
    assert utils.encode_uri_component('az09_$()+-') == 'az09_%24()%2B-'


def test_encode_attachment_id():
    assert utils.encode_attachment_id('d/e/f.txt') == 'd/e/f.txt'
    assert utils.encode_attachment_id('a0+$/9_()') == 'a0%2B%24/9_()'


def test_encode_document_id():
    assert utils.encode_document_id('some+id') == 'some%2Bid'
    assert utils.encode_document_id('_design/a/b/c') == '_design/a%2Fb%2Fc'
    assert utils.encode_document_id('_local/az09_$()+-') == '_local/az09_%24()%2B-'


def test_get_database_host():
    assert utils.get_database_host('https://foobar.com:5984/testdb') == 'https://foobar.com:5984'
    assert utils.get_database_host('http://u:p@foo.com/a/b/index.html?hey=yo') == 'http://u:p@foo.com'


def test_get_database_name():
    assert utils.get_database_name('http://foobar.com:5984/testdb') == 'testdb'
    assert utils.get_database_name('https://u:p@foo.com/a/b/index.html?hey=yo') == 'index.html'
    assert utils.get_database_name('http://foobar.com:5984/some%2Bid') == 'some%2Bid'


def test_query_method_kwargs():
    assert utils.query_method_kwargs({}) == ('GET', {})
    method, kwargs = utils.query_method_kwargs({'start_key': ['x'], 'endkey': 2})
    assert method == 'GET'
    assert kwargs == {'params': {'endkey': '2', 'start_key': '["x"]'}}


def test_query_method_kwargs_post_method():
    keys = [2, '10', True, 'foo']
    method, kwargs = utils.query_method_kwargs({'keys': keys})
    assert method == 'POST'
    assert kwargs == {'json': {'keys': keys}}


def test_raise_http_exception(mocker):
    status_codes = {
        400: exceptions.BadRequest,
        401: exceptions.Unauthorized,
        403: exceptions.Forbidden,
        404: exceptions.ResourceNotFound,
        405: exceptions.MethodNotAllowed,
        # 406: time2relax.NotAcceptable,
        409: exceptions.ResourceConflict,
        412: exceptions.PreconditionFailed,
        # 415: time2relax.BadContentType,
        # 416: time2relax.RequestedRangeNotSatisfiable,
        # 417: time2relax.ExpectationFailed,
        500: exceptions.ServerError,
        999: exceptions.HTTPError,
    }

    for code, ex in status_codes.items():
        mock_response = mocker.Mock()
        mock_response.status_code = code
        mock_response.json.return_value = {
            'error': 'error_{}'.format(code),
            'reason': 'test',
        }
        with pytest.raises(ex) as ex_info:
            utils.raise_http_exception(mock_response)
            assert ex_info.value.args == (
                mock_response.json.return_value,
                mock_response,
            )
