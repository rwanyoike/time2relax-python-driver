# -*- coding: utf-8 -*-

import pytest
from requests import ConnectionError


def test_bulk_docs(db):
    docs = [
        {'_id': '0'},
        {'_id': '1'},
        {'_id': '2'},
        {'_id': '3'},
    ]

    r = db.bulk_docs(docs)
    result = r.json()
    assert len(result) == 4

    for i, doc in enumerate(result):
        assert doc['id'] == docs[i]['_id']
        assert 'rev' in result[i]


def test_bulk_docs_params_new_edits(db):
    # No ``_rev`` and ``new_edits=false``
    docs = [{'_id': 'foo', 'integer': 1}]

    with pytest.raises(ConnectionError):
        db.bulk_docs(docs, {'new_edits': False})


def test_bulk_docs_kwargs(db):
    r = db.bulk_docs([], headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
