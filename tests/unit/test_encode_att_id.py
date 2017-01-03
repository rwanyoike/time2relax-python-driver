# -*- coding: utf-8 -*-


def test_encode_att_id(db):
    result = db._encode_att_id('d/e/f.txt')
    assert result == 'd/e/f.txt'


def test_encode_att_id_complex(db):
    result = db._encode_att_id('a0+$/9_()')
    assert result == 'a0%2B%24/9_()'
