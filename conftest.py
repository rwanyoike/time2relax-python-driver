# -*- coding: utf-8 -*-

import os
from posixpath import join as urljoin

import pytest

from time2relax import CouchDB, ResourceNotFound

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://localhost:5984/')


@pytest.fixture(scope='module')
def url():
    return urljoin(COUCHDB_URL, 'testdb')


@pytest.fixture(scope='module')
def cleanup(url):
    yield
    destroy(url)


@pytest.fixture()
def db(url, cleanup):
    destroy(url)
    yield CouchDB(url)


def destroy(url):
    try:
        db = CouchDB(url)
        db.destroy()
    except ResourceNotFound:
        pass
