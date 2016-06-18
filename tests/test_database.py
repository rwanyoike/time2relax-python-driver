# -*- coding: utf-8 -*-

from time2relax import Server, Database


def test_database_object():
    """Tests. Tests. Tests."""

    d = Database(Server(), 'test')
    t = '<{0} [{1}]>'.format(d.__class__.__name__, d.url)

    assert repr(d) == t
