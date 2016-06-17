# -*- coding: utf-8 -*-

from time2relax import Server


def test_server_object():
    """Tests. Tests. Tests."""

    s = Server()
    t = '<{0} [{1}]>'.format(s.__class__.__name__, s.url)

    assert repr(s) == t
