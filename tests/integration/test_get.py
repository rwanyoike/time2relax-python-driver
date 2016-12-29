# -*- coding: utf-8 -*-

from operator import itemgetter

import pytest

from time2relax import ResourceNotFound


def test_get(db):
    response = db.insert({'test': 'somestuff'})
    result = response.json()

    response = db.get(result['id'])
    doc = response.json()

    assert 'test' in doc

    with pytest.raises(ResourceNotFound) as ex:
        db.get(result['id'] + 'asdf')

    response = ex.value.response
    assert response.status_code == 404

    message = ex.value.response.json()
    assert message['reason'] == 'missing'
    assert message['error'] == 'not_found'


def test_get_design(db):
    response = db.insert({
        '_id': '_design/someid',
        'test': 'somestuff',
    })
    result = response.json()

    response = db.get(result['id'])
    doc = response.json()

    assert 'test' in doc


def test_get_local(db):
    response = db.insert({
        '_id': '_local/someid',
        'test': 'somestuff',
    })
    result = response.json()

    response = db.get(result['id'])
    doc = response.json()

    assert 'test' in doc


def test_get_params_rev(db):
    response = db.insert({'version': 'first'})
    result = response.json()

    db.insert({
        '_id': result['id'],
        '_rev': result['rev'],
        'version': 'second',
    })

    response = db.get(result['id'], {'rev': result['rev']})
    doc = response.json()

    assert doc['version'] == 'first'

    with pytest.raises(ResourceNotFound) as ex:
        db.get(result['id'], {'rev': '1-nonexistent-rev'})

    message = ex.value.response.json()
    assert message['error'] == 'not_found'
    assert message['reason'] == 'missing'


def test_get_params_open_revs_all(db):
    _put_conflicts(db)

    response = db.get('3', {'open_revs': 'all'})
    doc = response.json()

    revs = map(itemgetter('ok'), doc)
    revs = sorted(revs, key=itemgetter('_rev'))

    assert len(revs) == 3


def test_get_params_open_revs_list(db):
    _put_conflicts(db)

    response = db.get('3', {'open_revs': [
        '2-aaa',
        '5-nonexistent',
        '3-bbb',
    ]})
    doc = response.json()

    rev = map(lambda d: d['ok'] if 'ok' in d else d, doc)
    rev = sorted(rev, key=lambda d: d['_rev'] if '_rev' in d else 'z')

    assert len(rev) == 3
    assert rev[0]['_rev'] == '2-aaa'
    assert rev[1]['_rev'] == '3-bbb'
    assert rev[2]['missing'] == '5-nonexistent'


def test_get_kwargs(db):
    with pytest.raises(ResourceNotFound) as ex:
        db.get('null', headers={'X-Assert': 'true'})

    response = ex.value.response
    assert 'X-Assert' in response.request.headers


def _put_conflicts(db):
    response = db.insert({'_id': '3'})
    result = response.json()

    rev_id = result['rev'].split('-')[1]
    conflicts = [
        {
            '_id': '3',
            '_rev': '2-aaa',
            'value': 'x',
            '_revisions': {
                'start': 2,
                'ids': [
                    'aaa',
                    rev_id,
                ],
            },
        },
        {
            '_id': '3',
            '_rev': '3-bbb',
            'value': 'y',
            '_deleted': True,
            '_revisions': {
                'start': 3,
                'ids': [
                    'bbb',
                    'some',
                    rev_id,
                ],
            },
        },
        {
            '_id': '3',
            '_rev': '4-ccc',
            'value': 'z',
            '_revisions': {
                'start': 4,
                'ids': [
                    'ccc',
                    'even',
                    'more',
                    rev_id,
                ],
            },
        },
    ]

    db.bulk_docs(conflicts, {'new_edits': False})
