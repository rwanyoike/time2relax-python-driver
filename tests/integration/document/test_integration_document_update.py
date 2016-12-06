# -*- coding: utf-8 -*-

from conftest import insert_one_doc, select_one_doc
from time2relax import Database

FIXTURE = ['document', 'update']


def test_update(server, db_name):
    """Should update a document."""

    db = Database(server, db_name)
    insert_one_doc(db)

    # Update document '_rev'
    doc = select_one_doc(db).json()
    j = db.insert(doc).json()

    assert j['id'] == doc['_id']
    assert j['rev'] != doc['_rev']
