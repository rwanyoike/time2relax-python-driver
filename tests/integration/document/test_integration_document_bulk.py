# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['document', 'bulk']


def test_bulk(server, db_name):
    """Should bulk insert the documents."""

    db = Database(server, db_name)
    docs = [
        {'key': 'baz', 'name': 'bazzel'},
        {'key': 'bar', 'name': 'barry'},
    ]
    j = db.bulk(docs).json()

    assert len(j) == 2
    assert j[0]['id']
    assert j[1]['id']


def test_params(server, db_name):
    """Should use custom params in bulk."""

    db = Database(server, db_name)
    docs = [
        {'key': 'baz', 'name': 'bazzel'},
        {'key': 'bar', 'name': 'barry'},
    ]
    j = db.bulk(docs, {'new_edits': True}).json()

    assert len(j) == 2
    assert j[0]['id']
    assert j[1]['id']
