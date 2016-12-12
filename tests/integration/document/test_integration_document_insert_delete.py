# -*- coding: utf-8 -*-

import pytest

from conftest import insert_one_doc, select_one_doc
from time2relax import Database, ResourceConflict

FIXTURE = ['document', 'insert_delete']


def test_insert(server, db_name):
    """Should insert a document."""

    db = Database(server, db_name)
    j = insert_one_doc(db).json()

    assert j['ok'] is True


def test_conflict(server, db_name):
    """Should fail to insert again."""

    db = Database(server, db_name)

    with pytest.raises(ResourceConflict) as ex:
        insert_one_doc(db)

    assert 'conflict' in str(ex.value)
    assert ex.value.response.status_code == 409


def test_delete(server, db_name):
    """Should delete a document."""

    db = Database(server, db_name)

    # Update document '_rev'
    doc = select_one_doc(db).json()
    j = db.delete(doc).json()

    assert j['ok'] is True
