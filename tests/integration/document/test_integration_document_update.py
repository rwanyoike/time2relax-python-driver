# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['document', 'update']


def test_update(server, db_name):
    """Should update the document."""

    db = Database(server, db_name)
    # Insert a single doc
    doc_1 = {'_id': 'foobar', 'foo': 'baz'}
    rev = db.insert(doc_1).json()['rev']
    doc_2 = {'_id': 'foobar', '_rev': rev, 'foo': 'bar'}

    r = db.insert(doc_2)
    json = r.json()

    assert json['id'] == 'foobar'
    assert json['rev'] != rev
