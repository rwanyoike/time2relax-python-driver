# -*- coding: utf-8 -*-


def test_encode_uri_component(db):
    result = db._encode_uri_component('escaped%2F1')
    assert result == 'escaped%252F1'


def test_encode_uri_component_slash(db):
    result = db._encode_uri_component('a/b/c')
    assert result == 'a%2Fb%2Fc'


def test_encode_uri_component_complex(db):
    result = db._encode_uri_component('az09_$()+-')
    assert result == 'az09_%24()%2B-'
