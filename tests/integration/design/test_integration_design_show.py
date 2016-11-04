# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['design', 'show']


def test_insert(server, db_name):
    """Should insert a show ddoc."""

    db = Database(server, db_name)
    show = {
        '_id': '_design/people',
        'shows': {
            'singleDoc': """function(doc, req) {
  if (req.query.format === 'json' || !req.query.format) {
    return {
      body: JSON.stringify({
        name: doc.name,
        city: doc.city,
        format: 'json'
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    };
  }
  if (req.query.format === 'html') {
    return {
      body: 'Hello Clemens!',
      headers: {
        'Content-Type': 'text/html'
      }
    };
  }
}"""
        }
    }
    db.insert(show)

    docs = [
        {'_id': 'p_clemens', 'name': 'Clemens', 'city': 'Dresden'},
        {'_id': 'p_randall', 'name': 'Randall', 'city': 'San Francisco'},
        {'_id': 'p_nuno', 'name': 'Nuno', 'city': 'New York'},
    ]
    for i in docs:
        db.insert(i)


def test_show(server, db_name):
    """Should show the amazing clemens in json."""

    db = Database(server, db_name)
    r = db.ddoc_show('people', 'singleDoc', 'p_clemens')
    json = r.json()

    assert r.headers['Content-Type'] == 'application/json'
    assert json['name'] == 'Clemens'
    assert json['city'] == 'Dresden'
    assert json['format'] == 'json'


def test_html(server, db_name):
    """Should show the amazing clemens in html."""

    db = Database(server, db_name)
    r = db.ddoc_show('people', 'singleDoc', 'p_clemens', {'format': 'html'})

    assert r.headers['Content-Type'] == 'text/html'
    assert r.text == 'Hello Clemens!'
