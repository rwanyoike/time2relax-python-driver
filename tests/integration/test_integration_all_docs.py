# -*- coding: utf-8 -*-

from operator import itemgetter

import pytest

from time2relax import BadRequest

TEST_DOCS = [
    {'_id': '0', 'a': 1, 'b': 1},
    {'_id': '1', 'a': 2, 'b': 4},
    {'_id': '2', 'a': 3, 'b': 9},
    {'_id': '3', 'a': 4, 'b': 16},
]


def test_all_docs(db):
    db.bulk_docs(TEST_DOCS)
    r = db.all_docs()
    result = r.json()

    assert len(result['rows']) == 4
    for doc in result['rows']:
        assert 0 <= int(doc['id']) < 4


def test_all_docs_params_keys(db):
    db.bulk_docs(TEST_DOCS)
    keys = ['3', '1']
    r = db.all_docs({'keys': keys})

    assert r.request.method == 'POST'
    assert list(map(itemgetter('key'), r.json()['rows'])) == keys


def test_all_docs_params_startkey_endkey(db):
    docs = [
        {'_id': '"weird id!" a'},
        {'_id': '"weird id!" z'},
    ]
    db.bulk_docs(docs)
    params = {'startkey': docs[0]['_id'], 'endkey': docs[1]['_id']}
    r = db.all_docs(params)

    assert r.json()['total_rows'] == 2


def test_all_docs_params_startkey_endkey_synonyms(db):
    db.bulk_docs(TEST_DOCS)
    params = {'start_key': 'org.couchdb.user:', 'end_key': 'org.couchdb.user;'}
    r = db.all_docs(params)

    assert len(r.json()['rows']) == 0


def test_all_docs_params_key(db):
    db.bulk_docs(TEST_DOCS)
    r = db.all_docs({'key': '1'})

    assert len(r.json()['rows']) == 1
    with pytest.raises(BadRequest):
        params = {'key': '1', 'keys': ['1', '2']}
        db.all_docs(params)


def test_all_docs_kwargs(db):
    r = db.all_docs(headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
