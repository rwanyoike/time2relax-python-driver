# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['attachment', 'update']


def test_update(server, db_name):
    """Should update an attachment."""

    db = Database(server, db_name)
    db.insert({'_id': 'foobaz', 'foo': 'baz'})

    # Update document '_rev'
    doc = db.get('foobaz').json()
    db.att_insert(doc, 'att', 'Hello World!', 'text/plain')

    # Update document '_rev'
    doc = db.get('foobaz').json()
    db.att_insert(doc, 'att', bytearray(20), 'image/bmp')

    # Remove document '_rev'
    doc = {'_id': 'foobaz'}
    t = db.att_get(doc, 'att').text

    assert t.decode('unicode-escape') == str(bytearray(20))
