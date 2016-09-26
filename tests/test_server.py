# -*- coding: utf-8 -*-

from time2relax import Server


def test_server_object():
    """Tests. Tests. Tests."""

    server = Server()
    r = '<{0} [{1}]>'.format(server.__class__.__name__, server.url)

    assert repr(server) == r
