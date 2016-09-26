# -*- coding: utf-8 -*-

import json
import os
from urlparse import urljoin

import pytest
import yaml
from responses import RequestsMock

from time2relax.time2relax import Server, Database


@pytest.fixture(scope='session')
def config():
    """Loads the test config from the fs."""

    return load_fixture('config.yml')


@pytest.fixture(scope='module')
def responses(request, config):
    """Mocks the Python Requests library."""

    fixture = getattr(request.module, 'FIXTURE', None)
    rm = RequestsMock()

    if not fixture:
        return rm

    path = '{0}.yml'.format(os.path.join(*fixture))

    for i in load_fixture(path):
        i['url'] = urljoin(config['url'], i['url'])
        if 'json' in i:
            i['json'] = json.loads(i['json'])
        rm.add(**i)

    return rm


@pytest.fixture(scope='module')
def db_name(request):
    fixture = getattr(request.module, 'FIXTURE', None)

    if fixture:
        return '_'.join(fixture)

    return None


@pytest.fixture(scope='module', params=['mocked', 'server'])
def server(request, config, responses, db_name):
    """Loads a test-ready Server instance."""

    s = Server(config['url'])

    if request.param == 'mocked':
        # Start mocking requests
        responses.start()
    if db_name:
        s.create(db_name)

    yield s

    if db_name:
        s.delete(db_name)
    if request.param == 'mocked':
        # Stop mocking requests
        responses.stop()
        responses.reset()


def insert_docs(server, name, docs):
    """Inserts multiple CouchDB documents."""

    db = Database(server, name)

    for i in docs:
        db.insert(i)


@pytest.fixture()
def insert_one():
    """Inserts a single CouchDB document."""

    def insert(server, name):
        docs = [{'_id': 'foobaz', 'foo': 'baz'}]
        insert_docs(server, name, docs)

    return insert


@pytest.fixture()
def insert_three():
    """Inserts three CouchDB documents."""

    def insert(server, name):
        docs = [
            {'_id': 'foobar', 'foo': 'bar'},
            {'_id': 'barfoo', 'bar': 'foo'},
            {'_id': 'foobaz', 'foo': 'baz'},
        ]
        insert_docs(server, name, docs)

    return insert


def get_fixture_path(name):
    """Returns a fixture's filesystem path."""

    return os.path.join(os.path.dirname(__file__), 'tests', 'fixtures', name)


def load_fixture(name):
    """Loads a fixture from the filesystem."""

    with open(get_fixture_path(name)) as f:
        return yaml.load(f)
