# -*- coding: utf-8 -*-

from conftest import insert_docs
from time2relax.time2relax import Database

FIXTURE = ['document', 'list']


def test_list(server, db_name):
    """Should list the three documents."""

    db = Database(server, db_name)
    insert_docs(db)
    r = db.list()
    json = r.json()

    assert json['total_rows'] == 3


def test_params(server, db_name):
    """Should be able to use custom params in list."""

    db = Database(server, db_name)
    r = db.list({'limit': 1})
    json = r.json()

    assert json['total_rows'] == 3
    assert len(json['rows']) == 1


def test_startkey(server, db_name):
    """Should be able to list with a startkey."""

    db = Database(server, db_name)
    r = db.list({'startkey': 'c'})
    json = r.json()

    assert json['total_rows'] == 3
    assert len(json['rows']) == 2
    assert json['offset'] == 1
