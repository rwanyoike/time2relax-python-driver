# -*- coding: utf-8 -*-

from conftest import insert_three_docs
from time2relax import Database

FIXTURE = ['document', 'list']


def test_list(server, db_name):
    """Should list the documents."""

    db = Database(server, db_name)
    insert_three_docs(db)
    j = db.list().json()

    assert j['total_rows'] == 3


def test_params(server, db_name):
    """Should use custom params in list."""

    db = Database(server, db_name)
    j = db.list({'limit': 1}).json()

    assert j['total_rows'] == 3
    assert len(j['rows']) == 1


def test_startkey(server, db_name):
    """Should list with a 'startkey'."""

    db = Database(server, db_name)
    j = db.list({'startkey': 'c'}).json()

    assert j['total_rows'] == 3
    assert len(j['rows']) == 2
    assert j['offset'] == 1
