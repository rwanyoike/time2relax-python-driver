# -*- coding: utf-8 -*-

from conftest import insert_one_doc
from time2relax import Database

FIXTURE = ['document', 'get']


def test_get(server, db_name):
    """Should get the document."""

    db = Database(server, db_name)
    insert_one_doc(db)
    json = db.get('foobaz', {'revs_info': True}).json()

    assert json['_id'] == 'foobaz'
    assert json['_revs_info']
