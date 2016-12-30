# -*- coding: utf-8 -*-

from time2relax import CouchDB


def test_get_db_name():
    url = 'http://foobar.com:5984/testdb'
    assert CouchDB._get_db_name(url) == 'testdb'


def test_get_db_name_complex():
    url = 'http://user:pass@foo.com/baz/bar/index.html?hey=yo'
    assert CouchDB._get_db_name(url) == 'index.html'
