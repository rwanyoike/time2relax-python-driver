# -*- coding: utf-8 -*-

import os

from conftest import insert_view
from time2relax.time2relax import Database

FIXTURE = ['design', 'list']


def test_list(server, db_name):
    """Should get the people by running the ddoc."""

    db = Database(server, db_name)
    insert_view(db)
    params = {'key': ['Derek', 'San Francisco']}
    r = db.ddoc_list('people', 'by_name_and_city', 'my_list', params)

    assert r.text == 'Hello'
