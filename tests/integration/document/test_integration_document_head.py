# -*- coding: utf-8 -*-

from conftest import insert_one_doc
from time2relax import Database

FIXTURE = ['document', 'head']


def test_head(server, db_name):
    """Should fetch a document."""

    db = Database(server, db_name)
    _id = insert_one_doc(db).json()['id']
    t = db.head(_id).text

    assert not t
