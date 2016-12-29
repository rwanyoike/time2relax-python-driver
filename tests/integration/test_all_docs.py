# -*- coding: utf-8 -*-

from operator import itemgetter

import pytest

from time2relax import BadRequest

ORIGINAL_DOCS = [
    {'_id': '0', 'a': 1, 'b': 1},
    {'_id': '1', 'a': 2, 'b': 4},
    {'_id': '2', 'a': 3, 'b': 9},
    {'_id': '3', 'a': 4, 'b': 16},
]


def test_all_docs(db):
    db.bulk_docs(ORIGINAL_DOCS)
    response = db.all_docs()
    result = response.json()

    assert len(result['rows']) == 4

    for doc in result['rows']:
        assert 0 <= int(doc['id']) < 4


def test_all_docs_params_startkey(db):
    db.bulk_docs(ORIGINAL_DOCS)
    response = db.all_docs({
        'startkey': '2',
        'include_docs': True,
    })
    result = response.json()

    assert len(result['rows']) == 2
    assert result['rows'][0]['id'] == '2'


def test_all_docs_params_keys(db):
    db.bulk_docs(ORIGINAL_DOCS)
    keys = ['3', '1']
    response = db.all_docs({'keys': keys})
    result = response.json()

    assert list(map(itemgetter('key'), result['rows'])) == keys


def test_all_docs_params_keys_exception(db):
    db.bulk_docs(ORIGINAL_DOCS)

    with pytest.raises(BadRequest):
        db.all_docs({
            'keys': ['2', '0', '1000'],
            'startkey': 'a',
        })
        db.all_docs({
            'keys': [],
            'endkey': 'a',
        })


def test_all_docs_params_keys_empty(db):
    db.bulk_docs(ORIGINAL_DOCS)
    response = db.all_docs({'keys': []})
    result = response.json()

    assert len(result['rows']) == 0


def test_all_docs_params_startkey_endkey(db):
    docs = [
        {'_id': '"weird id!" a'},
        {'_id': '"weird id!" z'},
    ]
    db.bulk_docs(docs)
    response = db.all_docs({
        'startkey': docs[0]['_id'],
        'endkey': docs[1]['_id'],
    })
    result = response.json()

    assert result['total_rows'] == 2


def test_all_docs_params_aliases(db):
    db.bulk_docs(ORIGINAL_DOCS)
    response = db.all_docs({
        'start_key': 'org.couchdb.user:',
        'end_key': 'org.couchdb.user;',
    })
    result = response.json()

    assert len(result['rows']) == 0


def test_all_docs_params_key(db):
    db.bulk_docs(ORIGINAL_DOCS)
    response = db.all_docs({'key': '1'})
    result = response.json()

    assert len(result['rows']) == 1

    with pytest.raises(BadRequest):
        db.all_docs({
            'key': '1',
            'keys': ['1', '2'],
        })


def test_all_docs_kwargs(db):
    response = db.all_docs(headers={'X-Assert': 'true'})
    assert 'X-Assert' in response.request.headers
