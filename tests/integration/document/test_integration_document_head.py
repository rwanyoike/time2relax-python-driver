# -*- coding: utf-8 -*-

from conftest import insert_1doc
from time2relax.time2relax import Database

FIXTURE = ['document', 'head']


def test_head(server, db_name):
    """Should get a status code when you do head."""

    db = Database(server, db_name)
    insert_1doc(db)
    r = db.head('foobaz')

    assert not r.text
