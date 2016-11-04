# -*- coding: utf-8 -*-

FIXTURE = ['database', 'list']


def test_list(server, db_name):
    """Should list the correct databases."""

    r = server.list()
    json = r.json()

    assert db_name in json
