# -*- coding: utf-8 -*-

from time2relax import Server, Database


def test_database_object():
    """Tests. Tests. Tests."""

    database = Database(Server(), 'test')
    r = '<{0} [{1}]>'.format(database.__class__.__name__, database.name)

    assert repr(database) == r
