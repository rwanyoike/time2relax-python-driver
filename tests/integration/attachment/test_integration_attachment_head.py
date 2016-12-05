# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['attachment', 'head']


def test_head(server, db_name):
    """Should HEAD an attachment."""

    db = Database(server, db_name)
    db.insert({'_id': 'foobaz', 'foo': 'baz'})

    # Update document '_rev'
    doc = db.get('foobaz').json()
    db.att_insert(doc, 'att', 'Hello World!', 'text/plain')

    # Remove document '_rev'
    doc = {'_id': 'foobaz'}
    t = db.att_head(doc, 'att').text

    assert not t
