# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['attachment', 'get']


def test_get(server, db_name):
    """Should fetch an attachment."""

    db = Database(server, db_name)
    db.insert({'_id': 'foobaz', 'foo': 'baz'})

    # Update document '_rev'
    doc = db.get('foobaz').json()
    db.att_insert(doc, 'att', 'Hello World!', 'text/plain')

    # Remove document '_rev'
    doc = {'_id': 'foobaz'}
    t = db.att_get(doc, 'att').text

    assert t == 'Hello World!'
