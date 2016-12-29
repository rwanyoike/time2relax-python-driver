# -*- coding: utf-8 -*-

import pytest

from time2relax import ResourceNotFound


def test_remove(db):
    response = db.insert({'test': 'somestuff'})
    result = response.json()

    response = db.remove(result['id'], result['rev'])

    with pytest.raises(ResourceNotFound) as ex:
        db.get(result['id'])

    result = response.json()
    assert 'ok' in result

    message = ex.value.response.json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'deleted'


def test_remove_kwargs(db):
    response = db.insert({})
    result = response.json()

    response = db.remove(result['id'], result['rev'], params={},
                         headers={'X-Assert': 'true'})

    assert 'X-Assert' in response.request.headers
