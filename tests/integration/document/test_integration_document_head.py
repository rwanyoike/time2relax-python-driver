# -*- coding: utf-8 -*-

from time2relax.time2relax import Database

FIXTURE = ['document', 'head']


def test_head(server, db_name, insert_one):
    """Should get a status code when you do head."""

    insert_one(server, db_name)
    db = Database(server, db_name)

    r = db.head('foobaz')

    assert not r.text
