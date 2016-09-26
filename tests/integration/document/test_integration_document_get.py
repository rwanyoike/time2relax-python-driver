# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['document', 'get']


def test_get(server, db_name, insert_one):
    """Should get the document."""

    insert_one(server, db_name)
    db = Database(server, db_name)

    r = db.get('foobaz', {'revs_info': True})
    json = r.json()

    assert json['_id'] == 'foobaz'
    assert json['_revs_info']
