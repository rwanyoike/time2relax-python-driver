# -*- coding: utf-8 -*-

from time2relax import Server


def test_server__str__():
    """Tests. Tests. Tests."""

    server = Server()
    s = '<{0} [{1}]>'.format(type(server).__name__, server.url)

    assert str(server) == s
