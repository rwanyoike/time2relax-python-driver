# -*- coding: utf-8 -*-


def test_get_db_host(db):
    url = 'http://foobar.com:5984/testdb'
    assert db._get_db_host(url) == 'http://foobar.com:5984'


def test_get_db_host_complex(db):
    url = 'http://user:pass@foo.com/baz/bar/index.html?hey=yo'
    assert db._get_db_host(url) == 'http://user:pass@foo.com'
