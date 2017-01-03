# -*- coding: utf-8 -*-

import json

import pytest

from time2relax import ServerError


def test_ddoc_list(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "    emit(doc._id, 'value');"
                       "}",
            },
        },
        'lists': {
            'mylist': "function (head, req) {"
                      "    start({code: 500});"
                      "    send(JSON.stringify(getRow()));"
                      "    send('\\n');"
                      "    send('test');"
                      "    return 'Hello World!';"
                      "}",
        },
    })

    db.insert({'_id': 'testdoc'})

    with pytest.raises(ServerError) as ex:
        db.ddoc_list('test', 'mylist', 'myview')

    r = ex.value.args[1]
    assert r.headers['Transfer-Encoding'] == 'chunked'

    parts = r.text.split('\n')
    doc = json.loads(parts[0])
    assert doc == {'id': 'testdoc', 'key': 'testdoc', 'value': 'value'}
    assert parts[1] == 'testHello World!'


def test_ddoc_list_other_id(db):
    db.insert({
        '_id': '_design/test',
        'lists': {
            'mylist': "function (head, req) {"
                      "    send('test');"
                      "    return 'Hello World!';"
                      "}",
        },
    })
    db.insert({
        '_id': '_design/other',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "    emit(doc._id, 'value');"
                       "}",
            },
        },
    })

    db.insert({'_id': 'testdoc'})

    r = db.ddoc_list('test', 'mylist', 'myview', 'other')
    assert r.text == 'testHello World!'


def test_ddoc_list_kwargs(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "    emit(doc._id, 'value');"
                       "}",
            },
        },
        'lists': {
            'mylist': "function (head, req) {"
                      "    return 'Hello World!';"
                      "}",
        },
    })

    r = db.ddoc_list('test', 'mylist', 'myview', headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
