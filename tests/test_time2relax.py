from posixpath import join as urljoin

import pytest
from requests import Session

from time2relax import exceptions, time2relax

TEST_URL = "http://couchdb:5984/foobar"


def test_all_docs():
    result = time2relax.all_docs()
    assert result == ("GET", "_all_docs", {})


def test_all_docs_with_params():
    params = {"keys": ["abcd", True, 22]}
    result = time2relax.all_docs(params=params)
    assert result == (
        "POST",
        "_all_docs",
        {
            "json": params,
        },
    )


def test_bulk_docs():
    docs = [{"_id": "0"}, {"_id": "1"}, {"_id": "2"}]
    result = time2relax.bulk_docs(docs)
    assert result == (
        "POST",
        "_bulk_docs",
        {
            "json": {
                "docs": docs,
            },
        },
    )


def test_bulk_docs_with_json():
    result = time2relax.bulk_docs([], json={"new_edits": False})
    assert result == (
        "POST",
        "_bulk_docs",
        {
            "json": {
                "new_edits": False,
                "docs": [],
            },
        },
    )


def test_bulk_docs_with_json_none():
    result = time2relax.bulk_docs([], json=None)
    assert result == (
        "POST",
        "_bulk_docs",
        {
            "json": {
                "docs": [],
            },
        },
    )


def test_compact():
    result = time2relax.compact()
    assert result == (
        "POST",
        "_compact",
        {
            "headers": {
                "Content-Type": "application/json",
            },
        },
    )


def test_compact_with_headers():
    result = time2relax.compact(headers={"X-Assert": "true"})
    assert result == (
        "POST",
        "_compact",
        {
            "headers": {
                "Content-Type": "application/json",
                "X-Assert": "true",
            },
        },
    )


def test_compact_with_headers_none():
    result = time2relax.compact(headers=None)
    assert result == (
        "POST",
        "_compact",
        {
            "headers": {
                "Content-Type": "application/json",
            },
        },
    )


def test_ddoc_list():
    result = time2relax.ddoc_list("test", "mylist", "myview")
    assert result == ("GET", "_design/test/_list/mylist/myview", {})


def test_ddoc_list_with_other_id():
    result = time2relax.ddoc_list("test", "mylist", "myview", "other_id")
    assert result == ("GET", "_design/test/_list/mylist/other_id/myview", {})


def test_ddoc_show():
    result = time2relax.ddoc_show("test", "myshow")
    assert result == ("GET", "_design/test/_show/myshow", {})


def test_ddoc_show_with_doc_id():
    result = time2relax.ddoc_show("test", "myshow", "doc_id")
    assert result == ("GET", "_design/test/_show/myshow/doc_id", {})


def test_ddoc_view():
    result = time2relax.ddoc_view("test", "myview")
    assert result == ("GET", "_design/test/_view/myview", {})


def test_ddoc_view_with_params():
    params = {"keys": ["abcd", True, 22]}
    result = time2relax.ddoc_view("test", "myview", params=params)
    assert result == (
        "POST",
        "_design/test/_view/myview",
        {
            "json": params,
        },
    )


def test_destroy():
    result = time2relax.destroy()
    assert result == ("DELETE", "", {})


def test_get():
    result = time2relax.get("_design/someid")
    assert result == ("GET", "_design/someid", {})


def test_get_with_params():
    result = time2relax.get("_design/testid", params={"open_revs": ["2-aaa", "3-bbb"]})
    assert result == (
        "GET",
        "_design/testid",
        {
            "params": {
                "open_revs": '["2-aaa", "3-bbb"]',
            },
        },
    )


def test_get_with_params_all():
    params = {"open_revs": "all"}
    result = time2relax.get("_design/someid", params=params)
    assert result == (
        "GET",
        "_design/someid",
        {
            "params": params,
        },
    )


def test_get_with_params_none():
    result = time2relax.get("_design/testid", params=None)
    assert result == (
        "GET",
        "_design/testid",
        {
            "params": None,
        },
    )


def test_get_att():
    result = time2relax.get_att("doc", "att.txt")
    assert result == ("GET", "doc/att.txt", {})


def test_info():
    result = time2relax.info()
    assert result == ("GET", "", {})


def test_insert():
    doc = {"test": "somestuff"}
    result = time2relax.insert(doc)
    assert result == (
        "POST",
        "",
        {
            "json": doc,
        },
    )


def test_insert_put_method():
    doc = {"_id": "someid"}
    result = time2relax.insert(doc)
    assert result == (
        "PUT",
        "someid",
        {
            "json": doc,
        },
    )


def test_insert_att():
    result = time2relax.insert_att("doc", None, "att.txt", "Zm9v", "text/plain")
    assert result == (
        "PUT",
        "doc/att.txt",
        {
            "data": "Zm9v",
            "headers": {
                "Content-Type": "text/plain",
            },
        },
    )


def test_insert_att_with_doc_rev():
    result = time2relax.insert_att("doc", "1-5bfa2c9", "att.txt", "Zm9v", "text/plain")
    assert result == (
        "PUT",
        "doc/att.txt",
        {
            "data": "Zm9v",
            "headers": {
                "Content-Type": "text/plain",
            },
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_insert_att_with_params():
    result = time2relax.insert_att(
        "doc", "1-5bfa2c9", "att.txt", "Zm9v", "text/plain", params={"foo": "bar"}
    )
    assert result == (
        "PUT",
        "doc/att.txt",
        {
            "data": "Zm9v",
            "headers": {
                "Content-Type": "text/plain",
            },
            "params": {
                "rev": "1-5bfa2c9",
                "foo": "bar",
            },
        },
    )


def test_insert_att_with_params_none():
    result = time2relax.insert_att(
        "doc", "1-5bfa2c9", "att.txt", "Zm9v", "text/plain", params=None
    )
    assert result == (
        "PUT",
        "doc/att.txt",
        {
            "data": "Zm9v",
            "headers": {
                "Content-Type": "text/plain",
            },
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_insert_att_with_headers():
    result = time2relax.insert_att(
        "doc",
        "1-5bfa2c9",
        "att.txt",
        "Zm9v",
        "text/plain",
        headers={"X-Assert": "true"},
    )
    assert result == (
        "PUT",
        "doc/att.txt",
        {
            "data": "Zm9v",
            "headers": {
                "Content-Type": "text/plain",
                "X-Assert": "true",
            },
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_insert_att_with_headers_none():
    result = time2relax.insert_att(
        "doc", "1-5bfa2c9", "att.txt", "Zm9v", "text/plain", headers=None
    )
    assert result == (
        "PUT",
        "doc/att.txt",
        {
            "data": "Zm9v",
            "headers": {
                "Content-Type": "text/plain",
            },
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_remove():
    result = time2relax.remove("someid", "1-5bfa2c9")
    assert result == (
        "DELETE",
        "someid",
        {
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_remove_with_params():
    result = time2relax.remove("someid", "1-5bfa2c9", params={"foo": "bar"})
    assert result == (
        "DELETE",
        "someid",
        {
            "params": {
                "rev": "1-5bfa2c9",
                "foo": "bar",
            },
        },
    )


def test_remove_with_params_none():
    result = time2relax.remove("someid", "1-5bfa2c9", params=None)
    assert result == (
        "DELETE",
        "someid",
        {
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_remove_att():
    result = time2relax.remove_att("doc", "1-5bfa2c9", "att.txt")
    assert result == (
        "DELETE",
        "doc/att.txt",
        {
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_remove_att_with_params():
    result = time2relax.remove_att("doc", "1-5bfa2c9", "att.txt", params={"foo": "bar"})
    assert result == (
        "DELETE",
        "doc/att.txt",
        {
            "params": {
                "rev": "1-5bfa2c9",
                "foo": "bar",
            },
        },
    )


def test_remove_att_with_params_none():
    result = time2relax.remove_att("doc", "1-5bfa2c9", "att.txt", params=None)
    assert result == (
        "DELETE",
        "doc/att.txt",
        {
            "params": {
                "rev": "1-5bfa2c9",
            },
        },
    )


def test_replicate_to():
    source = "http://xxxx.db:5984/foo"
    target = "http://test.db:5984/bar"

    result = time2relax.replicate_to(source, target)
    assert result == (
        "POST",
        "http://xxxx.db:5984/_replicate",
        {
            "json": {
                "source": source,
                "target": target,
            },
        },
    )


def test_replicate_to_with_json():
    source = "http://xxxx.db:5984/foo"
    target = "http://test.db:5984/bar"

    result = time2relax.replicate_to(source, target, json={"foo": "bar"})
    assert result == (
        "POST",
        "http://xxxx.db:5984/_replicate",
        {
            "json": {
                "source": source,
                "target": target,
                "foo": "bar",
            },
        },
    )


def test_replicate_to_with_json_none():
    source = "http://xxxx.db:5984/foo"
    target = "http://test.db:5984/bar"

    result = time2relax.replicate_to(source, target, json=None)
    assert result == (
        "POST",
        "http://xxxx.db:5984/_replicate",
        {
            "json": {
                "source": source,
                "target": target,
            },
        },
    )


def test_request(mocker):
    mock_request = mocker.patch.object(Session, "request", autospec=True)
    mock_request.return_value.status_code = 200
    session = Session()

    result = time2relax.request(session, TEST_URL, "HEAD", "")
    assert result == mock_request.return_value
    mock_request.assert_called_with(session, "HEAD", TEST_URL)


def test_request_with_path(mocker):
    mock_request = mocker.patch.object(Session, "request", autospec=True)
    mock_request.return_value.status_code = 200
    session = Session()
    path = "_design/someid"

    result = time2relax.request(session, TEST_URL, "HEAD", path)
    assert result == mock_request.return_value
    mock_request.assert_called_with(session, "HEAD", urljoin(TEST_URL, path))


def test_request_with_path_absolute(mocker):
    mock_request = mocker.patch.object(Session, "request", autospec=True)
    mock_request.return_value.status_code = 200
    session = Session()
    path = "http://couchdb:5984/_replicate"

    result = time2relax.request(session, TEST_URL, "POST", path)
    assert result == mock_request.return_value
    mock_request.assert_called_with(session, "POST", path)


def test_request_with_params(mocker):
    mock_request = mocker.patch.object(Session, "request", autospec=True)
    mock_request.return_value.status_code = 200
    session = Session()

    result = time2relax.request(
        session,
        TEST_URL,
        "HEAD",
        "",
        params={
            "foo": "bar",
            "bool": True,
            "int": 21,
        },
    )
    assert result == mock_request.return_value
    mock_request.assert_called_with(
        session,
        "HEAD",
        TEST_URL,
        params={
            "foo": "bar",
            "bool": "true",
            "int": 21,
        },
    )


def test_request_with_params_int(mocker):
    mock_request = mocker.patch.object(Session, "request", autospec=True)
    mock_request.return_value.status_code = 200
    session = Session()

    result = time2relax.request(session, TEST_URL, "HEAD", "", params=42)
    assert result == mock_request.return_value
    mock_request.assert_called_with(session, "HEAD", TEST_URL, params=42)


def test_request_raise_exception(mocker):
    mock_request = mocker.patch.object(Session, "request", autospec=True)
    mock_request.side_effect = [mocker.MagicMock(status_code=412)]
    session = Session()

    with pytest.raises(exceptions.PreconditionFailed):
        time2relax.request(session, TEST_URL, "HEAD", "")
    mock_request.assert_called_with(session, "HEAD", TEST_URL)
