# -*- coding: utf-8 -*-

import pytest

from time2relax.errors import CouchDbError


def test_couchdb_error_object():
    """Tests. Tests. Tests."""

    message = {'error': 'time2relax', 'reason': 'CouchDB'}
    headers = {'Content-Type': 'relaxed'}
    status_code = 999

    with pytest.raises(CouchDbError) as ex:
        raise CouchDbError(message, headers, status_code)

    assert ex.value.message == message
    assert ex.value.headers == headers
    assert ex.value.status_code == status_code
