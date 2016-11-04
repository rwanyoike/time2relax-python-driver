# -*- coding: utf-8 -*-

from conftest import prepare_a_view
from time2relax import Database

FIXTURE = ['design', 'query']


def test_query(server, db_name):
    """Should respond with derek when asked for derek."""

    db = Database(server, db_name)
    prepare_a_view(db)
    params = {'key': ['Derek', 'San Francisco']}
    r1 = db.view('people', 'view', 'by_name_and_city', params)
    # Should have no issues when doing queries
    r2 = db.view('people', 'view', 'by_name_and_city', params)
    r3 = db.view('people', 'view', 'by_name_and_city', params)

    for i in [r1, r2, r3]:
        json = i.json()
        assert len(json['rows']) == 1
