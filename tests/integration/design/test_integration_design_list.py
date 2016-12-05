# -*- coding: utf-8 -*-

from conftest import prepare_a_view
from time2relax import Database

FIXTURE = ['design', 'list']


def test_list(server, db_name):
    """Should get the people by running the ddoc."""

    db = Database(server, db_name)
    prepare_a_view(db)
    params = {'key': ['Derek', 'San Francisco']}
    text = db.ddoc_list('people', 'by_name_and_city', 'my_list', params).text

    assert text == 'Hello'
