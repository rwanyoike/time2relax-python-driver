# -*- coding: utf-8 -*-

import json
import os
from urlparse import urljoin

import pytest
import yaml
from responses import RequestsMock

from time2relax.time2relax import Server


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
        i['url'] = urljoin(config['couch'], i['url'])
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

    s = Server(config['couch'])

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


def prepare_a_view(db):
    """Creates a ddoc and inserts some docs."""

    db.insert({
        '_id': '_design/people',
        'views': {
            'by_name_and_city': {
                'map': 'function(doc) { emit([doc.name, doc.city], doc._id); }'
            }
        },
        'lists': {
            'my_list': 'function(head, req) { send(\'Hello\'); }'
        }
    })

    docs = [
        {'_id': 'p_derek', 'name': 'Derek', 'city': 'San Francisco'},
        {'_id': 'p_randall', 'name': 'Randall', 'city': 'San Francisco'},
        {'_id': 'p_nuno', 'name': 'Nuno', 'city': 'London'},
    ]

    for i in docs:
        db.insert(i)


def insert_one_doc(db):
    """Inserts a single CouchDB document."""

    return db.insert({'_id': 'foobaz', 'foo': 'baz'})


def select_one_doc(db):
    """Selects a single CouchDB document."""

    return db.get('foobaz')


def insert_three_docs(db):
    """Inserts three CouchDB documents."""

    docs = [
        {'_id': 'foobar', 'foo': 'bar'},
        {'_id': 'barfoo', 'bar': 'foo'},
        {'_id': 'foobaz', 'foo': 'baz'},
    ]

    for i in docs:
        db.insert(i)


def get_fixture_path(name):
    """Returns a fixture's filesystem path."""

    return os.path.join(os.path.dirname(__file__), 'tests', 'fixtures', name)


def load_fixture(name):
    """Loads a fixture from the filesystem."""

    with open(get_fixture_path(name)) as f:
        return yaml.load(f)
