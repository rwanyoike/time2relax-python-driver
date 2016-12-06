# -*- coding: utf-8 -*-

FIXTURE = ['database', 'create_delete']


def test_create(server):
    """Should create a database."""

    assert server.create('az09_$()+-/').json()
    assert server.create('with/slash').json()


def test_delete(server):
    """Should delete a database."""

    assert server.delete('az09_$()+-/').json()
    assert server.delete('with/slash').json()
