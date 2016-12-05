# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['attachment', 'insert_delete']


def test_insert(server, db_name):
    """Should insert an attachment."""

    db = Database(server, db_name)
    db.insert({'_id': 'foobaz', 'foo': 'baz'})

    # Update document '_rev'
    doc = db.get('foobaz').json()
    j = db.att_insert(doc, 'att', 'Hello World!', 'text/plain').json()

    assert j['ok'] is True


def test_delete(server, db_name):
    """Should delete an attachment."""

    db = Database(server, db_name)

    # Update document '_rev'
    doc = db.get('foobaz').json()
    j = db.att_delete(doc, 'att').json()

    assert j['ok'] is True
