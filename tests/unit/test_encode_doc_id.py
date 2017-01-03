# -*- coding: utf-8 -*-


def test_encode_doc_id(db):
    result = db._encode_doc_id('some+id')
    assert result == 'some%2Bid'


def test_encode_doc_id_design(db):
    result = db._encode_doc_id('_design/a/b/c')
    assert result == '_design/a%2Fb%2Fc'


def test_encode_doc_id_local(db):
    result = db._encode_doc_id('_local/az09_$()+-')
    assert result == '_local/az09_%24()%2B-'
