# -*- coding: utf-8 -*-

FIXTURE = ['database', 'get']


def test_get(server, db_name):
    """Should be able to fetch the database."""

    r = server.get(db_name)
    json = r.json()

    assert json['db_name'] == db_name
    assert json['doc_count'] == 0
