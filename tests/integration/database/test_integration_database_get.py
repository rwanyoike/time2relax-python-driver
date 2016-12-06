# -*- coding: utf-8 -*-

FIXTURE = ['database', 'get']


def test_get(server, db_name):
    """Should fetch a database."""

    j = server.get(db_name).json()

    assert j['doc_count'] == 0
