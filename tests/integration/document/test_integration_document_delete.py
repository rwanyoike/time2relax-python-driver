# -*- coding: utf-8 -*-

from time2relax.time2relax import Database

FIXTURE = ['document', 'delete']


def test_delete(server, db_name):
    """Should delete a document."""

    db = Database(server, db_name)
    # Insert a single doc
    doc = {'_id': 'foobaz', 'foo': 'baz'}
    rev = db.insert(doc).json()['rev']

    db.delete('foobaz', rev)
