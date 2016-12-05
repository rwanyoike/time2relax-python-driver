# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['attachment', 'delete']


def test_delete(server, db_name):
    """Should delete an attachment."""

    db = Database(server, db_name)
    db.insert({'_id': 'foobaz', 'foo': 'baz'})

    # Update document '_rev'
    doc = db.get('foobaz').json()
    db.att_insert(doc, 'att', 'Hello World!', 'text/plain')

    # Update document '_rev'
    doc = db.get('foobaz').json()
    j = db.att_delete(doc, 'att').json()

    assert j['ok'] is True
