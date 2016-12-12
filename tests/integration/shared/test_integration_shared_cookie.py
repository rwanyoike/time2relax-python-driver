# -*- coding: utf-8 -*-

import os
from requests.compat import urlparse

from time2relax import Database

FIXTURE = ['shared', 'cookie']


def test_cookie(config, server):
    """Should setup admin and login."""

    pr = urlparse(config['admin'])
    username = pr.username
    password = pr.password

    url = os.path.join('_config', 'admins', username)
    server.request('PUT', url, json=password)
    h = server.auth(username, password).headers

    assert h['set-cookie']


def test_insert(server, db_name):
    """Should insert with a cookie."""

    db = Database(server, db_name)
    db.insert({})


def test_session(config, server):
    """Should get the auth session."""

    pr = urlparse(config['admin'])
    username = pr.username
    j = server.session().json()

    assert j['userCtx']['name'] == username


def test_delete(config, server):
    """Should restore noadmin (for tests)."""

    pr = urlparse(config['admin'])
    username = pr.username

    url = os.path.join('_config', 'admins', username)
    server.request('DELETE', url)
