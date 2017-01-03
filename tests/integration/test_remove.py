# -*- coding: utf-8 -*-

import pytest

from time2relax import ResourceNotFound


def test_remove(db):
    r = db.insert({'test': 'somestuff'})
    result = r.json()

    r = db.remove(result['id'], result['rev'])

    with pytest.raises(ResourceNotFound) as ex:
        db.get(result['id'])

    result = r.json()
    assert 'ok' in result

    message = ex.value.args[1].json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'deleted'


def test_remove_kwargs(db):
    r = db.insert({})
    result = r.json()

    r = db.remove(result['id'], result['rev'], params={},
                  headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
