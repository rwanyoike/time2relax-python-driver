# -*- coding: utf-8 -*-

from time2relax.time2relax import Database

FIXTURE = ['database', 'replicate']


def test_replicate(server, db_name, insert_three):
    """Should be able to replicate three docs."""

    insert_three(server, db_name)
    # Create a database replica
    server.create('database_replica')
    server.replicate(db_name, 'database_replica')
    db = Database(server, 'database_replica')

    r = db.list()
    json = r.json()

    assert json['total_rows'] == 3


def test_params(server, db_name):
    """Should be able to replicate with params."""

    server.replicate(db_name, 'database_replica', {'continuous': False})


def test_destroy(server):
    """Should destroy the extra databases."""

    server.delete('database_replica')
