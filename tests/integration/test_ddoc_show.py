# -*- coding: utf-8 -*-


def test_ddoc_show(db):
    db.insert({
        '_id': '_design/test',
        'shows': {
            'myshow': "function (doc, req) {"
                      "    if (!doc) {"
                      "        return {body: 'no doc'}"
                      "    } else {"
                      "        return {body: doc.description}"
                      "    }"
                      "}",
        },
    })

    r = db.ddoc_show('test', 'myshow')
    assert r.headers['Content-Type'] == 'text/html; charset=utf-8'
    assert r.text == 'no doc'


def test_ddoc_show_doc_id(db):
    db.insert({
        '_id': '_design/test',
        'shows': {
            'myshow': "function (doc, req) {"
                      "    if (!doc) {"
                      "        return {body: 'no doc'}"
                      "    } else {"
                      "        return {body: doc.description}"
                      "    }"
                      "}",
        },
    })

    db.insert({'_id': 'mydoc', 'description': 'Hello World!'})

    r = db.ddoc_show('test', 'myshow', 'mydoc')
    assert r.text == 'Hello World!'


def test_ddoc_show_kwargs(db):
    db.insert({
        '_id': '_design/test',
        'shows': {
            'myshow': "function (doc, req) {"
                      "    return {body: 'no doc'}"
                      "}",
        },
    })

    r = db.ddoc_show('test', 'myshow', headers={'X-Assert': 'true'})
    assert 'X-Assert' in r.request.headers
