# -*- coding: utf-8 -*-

from conftest import insert_one_doc, select_one_doc
from time2relax import Database

FIXTURE = ['database', 'compact']


def test_compact(server, db_name):
    """Should run a compaction."""

    db = Database(server, db_name)
    insert_one_doc(db)

    # Update document '_rev'
    doc = select_one_doc(db).json()
    # Delete the document
    db.delete(doc)

    server.compact(db_name)
    j = server.get(db_name).json()

    assert j['doc_count'] == 0
    assert j['doc_del_count'] == 1
