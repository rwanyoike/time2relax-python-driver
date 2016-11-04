# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['document', 'bulk']


def test_bulk(server, db_name):
    """Should be able to bulk insert two docs."""

    db = Database(server, db_name)
    docs = [
        {'key': 'baz', 'name': 'bazzel'},
        {'key': 'bar', 'name': 'barry'},
    ]
    r = db.bulk(docs)
    json = r.json()

    assert len(json) == 2
    assert json[0]['id']
    assert json[1]['id']


def test_params(server, db_name):
    """Should be able to use custom params in bulk."""

    db = Database(server, db_name)
    docs = [
        {'key': 'baz', 'name': 'bazzel'},
        {'key': 'bar', 'name': 'barry'},
    ]
    r = db.bulk(docs, {'new_edits': True})
    json = r.json()

    assert len(json) == 2
    assert json[0]['id']
    assert json[1]['id']
