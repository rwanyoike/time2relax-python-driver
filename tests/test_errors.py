# -*- coding: utf-8 -*-

import pytest

from time2relax.errors import CouchDbError


def test_couchdb_error_message():
    """Tests. Tests. Tests."""

    message = {
        'error': 'time2relax',
        'reason': 'CouchDB',
    }

    with pytest.raises(CouchDbError) as excinfo:
        raise CouchDbError(message)

    assert excinfo.value.message == message
    assert excinfo.value.headers is None
    assert excinfo.value.status_code is None


def test_couchdb_error_headers():
    """Tests. Tests. Tests."""

    headers = {'Content-Type': 'relaxed'}

    with pytest.raises(CouchDbError) as excinfo:
        raise CouchDbError(None, headers=headers)

    assert excinfo.value.message is None
    assert excinfo.value.headers == headers
    assert excinfo.value.status_code is None


def test_couchdb_error_status_code():
    """Tests. Tests. Tests."""

    status_code = 999

    with pytest.raises(CouchDbError) as excinfo:
        raise CouchDbError(None, status_code=status_code)

    assert excinfo.value.message is None
    assert excinfo.value.headers is None
    assert excinfo.value.status_code == status_code
