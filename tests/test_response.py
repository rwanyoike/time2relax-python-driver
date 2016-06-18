# -*- coding: utf-8 -*-

from time2relax.time2relax import Response


def test_response_object():
    """Tests. Tests. Tests."""

    r = Response('http://example.com', {}, {})
    s = '<{0} [{1}]>'.format(r.__class__.__name__, r.url)

    assert repr(r) == s
