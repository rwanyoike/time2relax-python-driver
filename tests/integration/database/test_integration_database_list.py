# -*- coding: utf-8 -*-

FIXTURE = ['database', 'list']


def test_list(server, db_name):
    """Should list the correct databases."""

    r = server.list()
    json = r.json()

    assert len(json) == 3

    for i in ['_replicator', '_users', db_name]:
        assert i in json
