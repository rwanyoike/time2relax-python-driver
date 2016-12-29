# -*- coding: utf-8 -*-

import pytest

from time2relax import ResourceNotFound


def test_remove_att(db):
    response = db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    result = response.json()

    response = db.remove_att('doc', 'att', result['rev'])

    with pytest.raises(ResourceNotFound) as ex:
        db.get_att('doc', 'att')

    result = response.json()
    assert 'ok' in result

    message = ex.value.response.json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'Document is missing attachment'


def test_remove_att_params(db):
    response = db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    result = response.json()

    response = db.remove_att('doc', 'att', result['rev'],
                             params={'x-assert': True})

    assert 'x-assert' in response.request.url


def test_remove_att_kwargs(db):
    response = db.insert_att('doc', 'att', None, 'Zm9v', 'text/plain')
    result = response.json()

    response = db.remove_att('doc', 'att', result['rev'],
                             headers={'X-Assert': 'true'})

    assert 'X-Assert' in response.request.headers
