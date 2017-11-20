# -*- coding: utf-8 -*-

import pytest

from time2relax import ResourceNotFound


def test_destroy(db):
    db.insert({'_id': 'cleanname'})
    db.destroy()

    with pytest.raises(ResourceNotFound):
        db.get('cleanname')


def test_destroy_kwargs(db):
    with pytest.raises(ResourceNotFound) as ex:
        db.destroy(headers={'X-Assert': 'true'})

    r = ex.value.args[1]
    assert 'X-Assert' in r.request.headers
