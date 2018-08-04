import pytest
from requests import RequestException

from time2relax.models import CouchDB


def test_couchdb():
    db = CouchDB('https://u:p@test.db/a/b/index.html?e=f', create_db=False)
    assert db.host == 'https://u:p@test.db'
    assert db.name == 'index.html'
    assert db.url == 'https://u:p@test.db/index.html'
    assert db.create_db is False
    assert db.session.headers['Accept'] == 'application/json'

    # Test default create_db value and __repr__
    db = CouchDB('http://couchdb:5984/foobar')
    assert db.create_db is True
    assert repr(db) == '<CouchDB [{}]>'.format(db.url)


def test_couchdb_raise_exception():
    for url in ['', 'http://', 'http://user:pass']:
        with pytest.raises(RequestException):
            CouchDB(url)
