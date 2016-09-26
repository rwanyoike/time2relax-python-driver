# -*- coding: utf-8 -*-

import pytest
from requests.models import Response

from time2relax.errors import CouchDbError


def test_couchdb_error_object():
    """Tests. Tests. Tests."""

    message = {'error': 'time2relax', 'reason': 'CouchDB'}

    with pytest.raises(CouchDbError) as ex:
        raise CouchDbError(message, Response())

    assert ex.value.message == message
