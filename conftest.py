# -*- coding: utf-8 -*-

import os

import pytest

from time2relax import CouchDB, ResourceNotFound

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


@pytest.fixture(scope='module')
def test_url():
    url = os.path.join(COUCHDB_URL, 'testdb')
    return url


@pytest.fixture(scope='module')
def cleanup(test_url):
    yield
    destroy(test_url)


@pytest.fixture()
def db(test_url, cleanup):
    destroy(test_url)
    yield CouchDB(test_url)


def destroy(test_url):
    try:
        db = CouchDB(test_url)
        db.destroy()
    except ResourceNotFound:
        pass
