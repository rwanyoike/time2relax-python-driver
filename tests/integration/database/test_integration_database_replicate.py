# -*- coding: utf-8 -*-

from conftest import insert_three_docs
from time2relax import Database

FIXTURE = ['database', 'replicate']
DATABASE_REPLICA = 'database_replica'


def test_replicate(server, db_name):
    """Should be able to replicate three docs."""

    insert_three_docs(Database(server, db_name))
    # Create a database replica
    server.create(DATABASE_REPLICA)
    server.replicate(db_name, DATABASE_REPLICA)
    db = Database(server, DATABASE_REPLICA)
    json = db.list().json()

    assert json['total_rows'] == 3


def test_params(server, db_name):
    """Should be able to replicate with params."""

    server.replicate(db_name, DATABASE_REPLICA, {'continuous': False})


def test_destroy(server):
    """Should destroy the extra database."""

    server.delete(DATABASE_REPLICA)
