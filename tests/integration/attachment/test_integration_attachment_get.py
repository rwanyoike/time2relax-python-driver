# -*- coding: utf-8 -*-

from conftest import insert_one_doc, select_one_doc
from time2relax import Database

FIXTURE = ['attachment', 'get']


def test_get(server, db_name):
    """Should fetch an attachment."""

    db = Database(server, db_name)
    insert_one_doc(db)

    # Update document '_rev'
    doc = select_one_doc(db).json()
    db.att_insert(doc, 'att', 'Hello World!', 'text/plain')

    # Remove document '_rev'
    del doc['_rev']
    t = db.att_get(doc, 'att').text

    assert t == 'Hello World!'
