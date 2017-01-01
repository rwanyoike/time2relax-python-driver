# -*- coding: utf-8 -*-

import pytest

from time2relax import ResourceNotFound


def test_remove_att(db):
    r = db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    result = r.json()

    r = db.remove_att('doc', result['rev'], 'att.txt')

    with pytest.raises(ResourceNotFound) as ex:
        db.get_att('doc', 'att.txt')

    result = r.json()
    assert 'ok' in result

    message = ex.value.response.json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'Document is missing attachment'


def test_remove_att_params(db):
    r = db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    result = r.json()

    r = db.remove_att('doc', result['rev'], 'att.txt',
                      params={'x-assert': True})
    assert 'x-assert' in r.request.url


def test_remove_att_kwargs(db):
    r = db.insert_att('doc', None, 'att.txt', 'Zm9v', 'text/plain')
    result = r.json()

    r = db.remove_att('doc', result['rev'], 'att.txt',
                      headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
