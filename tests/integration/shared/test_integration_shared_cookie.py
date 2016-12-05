# -*- coding: utf-8 -*-

import os
from urlparse import urlparse

from time2relax import Database

FIXTURE = ['shared', 'cookie']


def test_cookie(config, server):
    """Should be able to setup admin and login."""

    pr = urlparse(config['admin'])
    username = pr.username
    password = pr.password
    url = os.path.join('_config', 'admins', username)
    server.request('PUT', url, json=password)
    headers = server.auth(username, password).headers

    assert headers['set-cookie']


def test_insert(server, db_name):
    """Should be able to insert with a cookie."""

    db = Database(server, db_name)
    db.insert({})


def test_session(config, server):
    """Should be able to get the session."""

    pr = urlparse(config['admin'])
    username = pr.username
    json = server.session().json()

    assert json['userCtx']['name'] == username


def test_delete(config, server):
    """Should restore noadmin for other tests."""

    pr = urlparse(config['admin'])
    username = pr.username
    url = os.path.join('_config', 'admins', username)
    server.request('DELETE', url)
