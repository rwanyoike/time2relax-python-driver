# -*- coding: utf-8 -*-

import pytest

from time2relax import CouchDB, ServerError


def test_replicate_to(db):
    db.insert({'test': 'somestuff'})
    db.insert({'test': 'somestuff'})
    db.insert({'test': 'somestuff'})

    db2 = CouchDB(db.host + '/testdb2')

    with pytest.raises(ServerError) as ex:
        db.replicate_to(db2.url)

    message = ex.value.response.json()
    assert message['error'] == 'db_not_found'
    assert message['reason'] == 'could not open {0}/'.format(db2.url)

    db2.request('HEAD', db2.url)  # setup db
    db.replicate_to(db2.url)

    r = db2.info()
    db2.destroy()

    result = r.json()
    assert result['doc_count'] == 3


def test_replicate_to_kwargs(db):
    db2 = CouchDB(db.host + '/testdb2')
    db2.request('HEAD', db2.url)  # setup db

    r = db.replicate_to(db2.url, json={}, headers={'X-Assert': 'true'})
    db2.destroy()

    assert 'X-Assert' in r.request.headers
