# -*- coding: utf-8 -*-

from conftest import insert_three_docs
from time2relax import Database

FIXTURE = ['database', 'replicate']
REPLICA = 'database_replica'


def test_replicate(server, db_name):
    """Should replicate the documents."""

    db = Database(server, db_name)
    insert_three_docs(db)

    # Create a database replica
    server.create(REPLICA)
    server.replicate(db_name, REPLICA, {'continuous': False})

    db = Database(server, REPLICA)
    j = db.list().json()

    assert j['total_rows'] == 3


def test_delete(server):
    """Should delete the replica."""

    assert server.delete(REPLICA).json()
