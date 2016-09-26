# -*- coding: utf-8 -*-

import pytest

from time2relax import Database
from time2relax.errors import ResourceConflict

FIXTURE = ['document', 'insert']


def test_insert(server, db_name):
    """Should insert a simple document."""

    db = Database(server, db_name)
    doc = {'_id': 'foobaz', 'foo': 'baz'}

    r = db.insert(doc)
    json = r.json()

    assert json['id'] == doc['_id']


def test_conflict(server, db_name):
    """Should fail to insert again since it already exists."""

    db = Database(server, db_name)

    with pytest.raises(ResourceConflict) as ex:
        doc = {'_id': 'foobaz', 'foo': 'baz'}
        db.insert(doc)

    assert ex.value.message['error'] == 'conflict'
    assert ex.value.response.status_code == 409


def test_params(server, db_name):
    """Should be able to use custom params in insert."""

    db = Database(server, db_name)
    rev = db.get('foobaz').json()['_rev']
    doc = {'_id': 'foobaz', '_rev': rev, 'foo': 'baz'}

    r = db.insert(doc, {'new_edits': False})
    json = r.json()

    assert json['id'] == doc['_id']
    assert json['rev'] == rev
