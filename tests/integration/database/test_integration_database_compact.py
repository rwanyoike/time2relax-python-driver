# -*- coding: utf-8 -*-

from time2relax import Database

FIXTURE = ['database', 'compact']


def test_compact(server, db_name):
    """Should have run the compaction."""

    db = Database(server, db_name)
    # Insert a single doc
    rev = db.insert({'_id': 'goofy', 'foo': 'baz'}).json()['rev']
    # Delete a single doc
    db.delete('goofy', rev)

    server.compact(db_name)
    r = server.get(db_name)
    json = r.json()

    assert json['doc_count'] == 0
    assert json['doc_del_count'] == 1
    assert json['update_seq'] == 2


def test_confirm(server, db_name):
    """Should finish compaction before ending."""

    r = server.get(db_name)
    json = r.json()

    assert json['compact_running'] == False
