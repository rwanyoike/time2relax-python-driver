# -*- coding: utf-8 -*-

FIXTURE = ['database', 'create_delete']


def test_create(server):
    """Should be able to create databases."""

    server.create('az09_$()+-/')
    server.create('with/slash')


def test_delete(server):
    """Must delete the databases we created."""

    server.delete('az09_$()+-/')
    server.delete('with/slash')
