# -*- coding: utf-8 -*-

from conftest import insert_one_doc
from time2relax import Database

FIXTURE = ['document', 'get']


def test_get(server, db_name):
    """Should fetch a document."""

    db = Database(server, db_name)
    _id = insert_one_doc(db).json()['id']
    j = db.get(_id, {'revs_info': True}).json()

    assert j['_id'] == _id
    assert j['_revs_info']
