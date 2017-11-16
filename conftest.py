# -*- coding: utf-8 -*-

import os
from posixpath import join as urljoin

import pytest

from time2relax import CouchDB, ResourceNotFound

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


def destroy_db(database_url):
    """Destroy any leftover databases."""
    try:
        CouchDB(database_url).destroy()
    except ResourceNotFound:
        pass


@pytest.fixture(scope='module')
def database_url():
    return urljoin(COUCHDB_URL, 'testdb')


@pytest.fixture(scope='module')
def cleanup(database_url):
    # This is a scope=module fixture
    yield
    destroy_db(database_url)


@pytest.fixture()
def db(database_url, cleanup):
    destroy_db(database_url)
    # Provide the fixture value
    yield CouchDB(database_url)
