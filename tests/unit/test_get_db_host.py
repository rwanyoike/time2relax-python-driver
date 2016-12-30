# -*- coding: utf-8 -*-

from time2relax import CouchDB


def test_get_db_host():
    url = 'http://foobar.com:5984/testdb'
    assert CouchDB._get_db_host(url) == 'http://foobar.com:5984'


def test_get_db_host_complex():
    url = 'http://user:pass@foo.com/baz/bar/index.html?hey=yo'
    assert CouchDB._get_db_host(url) == 'http://user:pass@foo.com'
