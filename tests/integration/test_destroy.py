# -*- coding: utf-8 -*-

import pytest

from time2relax import CouchDBError, ResourceNotFound


def test_destroy(db):
    db.insert({'_id': 'cleanname'})
    db.destroy()

    assert db._destroyed is True

    with pytest.raises(CouchDBError):
        db.get('cleanname')


def test_destroy_kwargs(db):
    with pytest.raises(ResourceNotFound) as ex:
        db.destroy(headers={'X-Assert': 'true'})

    response = ex.value.response
    assert 'X-Assert' in response.request.headers
