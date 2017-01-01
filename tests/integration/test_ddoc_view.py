# -*- coding: utf-8 -*-


def test_ddoc_view(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "    emit(doc.foo, doc);"
                       "}",
            },
        },
    })
    db.bulk_docs([
        {'foo': 'bar'},
        {'_id': 'volatile', 'foo': 'baz'},
    ])

    r = db.get('volatile')
    result = r.json()
    db.remove(result['_id'], result['_rev'])

    params = {'reduce': False, 'include_docs': True}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()

    assert len(result['rows']) == 1
    assert result['total_rows'] == 1

    for row in result['rows']:
        assert row['id']
        assert row['key']
        assert row['value']
        assert row['value']['_rev']
        assert row['doc']
        assert row['doc']['_rev']


def test_ddoc_view_params_startkey_endkey(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "   emit(doc.key, doc);"
                       "}",
            },
        },
    })
    db.bulk_docs([
        {'key': 'key1'},
        {'key': 'key2'},
        {'key': 'key3'},
        {'key': 'key4'},
        {'key': 'key5'},
    ])

    params = {'reduce': False, 'startkey': 'key2'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 4

    params = {'reduce': False, 'startkey': 'key3'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 3

    params = {'reduce': False, 'startkey': 'key2', 'endkey': 'key3'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 2

    params = {'reduce': False, 'startkey': 'key4', 'endkey': 'key4'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 1


def test_ddoc_view_params_startkey_endkey_synonyms(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "   emit(doc.key, doc);"
                       "}",
            },
        },
    })
    db.bulk_docs([
        {'key': 'key1'},
        {'key': 'key2'},
        {'key': 'key3'},
        {'key': 'key4'},
        {'key': 'key5'},
    ])

    params = {'reduce': False, 'start_key': 'key2'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 4

    params = {'reduce': False, 'start_key': 'key3'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 3

    params = {'reduce': False, 'start_key': 'key2', 'end_key': 'key3'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 2

    params = {'reduce': False, 'start_key': 'key4', 'end_key': 'key4'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 1


def test_ddoc_view_params_key(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "   emit(doc.key, doc);"
                       "}",
            },
        },
    })
    db.bulk_docs([
        {'key': 'key1'},
        {'key': 'key2'},
        {'key': 'key3'},
        {'key': 'key3'},
    ])

    params = {'reduce': False, 'key': 'key2'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 1

    params = {'reduce': False, 'key': 'key3'}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert len(result['rows']) == 2


def test_ddoc_view_params_reduce(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "   emit(null, doc.val);"
                       "}",
                'reduce': '_sum',
            },
        },
    })
    db.bulk_docs([
        {'_id': '1', 'val': 2},
        {'_id': '2', 'val': [1, 2, 3, 4]},
        {'_id': '3', 'val': [3, 4]},
        {'_id': '4', 'val': 1},
    ])

    params = {'reduce': True, 'group': True}
    r = db.ddoc_view('test', 'myview', params)
    result = r.json()
    assert result['rows'] == [{'key': None, 'value': [7, 6, 3, 4]}]


def test_ddoc_view_params_keys(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "   emit(doc.foo, doc.foo);"
                       "}",
            },
        },
    })
    db.bulk_docs([
        {'foo': {'key2': 'value2'}},
        {'foo': {'key1': 'value1'}},
        {'foo': [0, 0]},
        {'foo': ['test', 1]},
        {'foo': [0, False]},
    ])

    keys = [
        {'key': 'missing'},
        ['test', 1],
        {'key1': 'value1'},
        ['missing'],
        [0, 0],
    ]
    r = db.ddoc_view('test', 'myview', {'keys': keys})
    result = r.json()

    assert r.request.method == 'POST'
    assert len(result['rows']) == 3
    assert result['rows'][0]['value'] == keys[1]
    assert result['rows'][1]['value'] == keys[2]
    assert result['rows'][2]['value'] == keys[4]


def test_ddoc_view_kwargs(db):
    db.insert({
        '_id': '_design/test',
        'views': {
            'myview': {
                'map': "function (doc) {"
                       "    emit(doc);"
                       "}",
            },
        },
    })

    r = db.ddoc_view('test', 'myview', headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
