# -*- coding: utf-8 -*-

from conftest import insert_three_docs
from time2relax import Database

FIXTURE = ['document', 'list']


def test_list(server, db_name):
    """Should list the three documents."""

    db = Database(server, db_name)
    insert_three_docs(db)
    json = db.list().json()

    assert json['total_rows'] == 3


def test_params(server, db_name):
    """Should be able to use custom params in list."""

    db = Database(server, db_name)
    json = db.list({'limit': 1}).json()

    assert json['total_rows'] == 3
    assert len(json['rows']) == 1


def test_startkey(server, db_name):
    """Should be able to list with a startkey."""

    db = Database(server, db_name)
    json = db.list({'startkey': 'c'}).json()

    assert json['total_rows'] == 3
    assert len(json['rows']) == 2
    assert json['offset'] == 1
