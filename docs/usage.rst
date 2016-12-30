=====
Usage
=====

To use time2relax in a project::

    >>> import time2relax

Create a database
-----------------

This method creates a database or opens an existing one::

    >>> db = time2relax.CouchDB('http://localhost:5984/dbname')

Initially ``CouchDB`` checks if the database exists, and tries to create it if
it does not exist yet. You can use ``skip_setup`` to skip this setup::

    >>> db = time2relax.CouchDB('http://localhost:5984/dbname', skip_setup=True)

Delete a database
-----------------

Delete the database::

    >>> db.destroy()
    <Response [200]>

Create/update a document
------------------------

Create a new document or update an existing document. If the document already
exists, you must specify its revision ``_rev``, otherwise a conflict will
occur.

There are some `restrictions on valid property names`_ of the documents.

Create a new doc with an ``_id`` of ``'mydoc'``::

    >>> db.insert({'_id': 'mydoc', 'title': 'Heros'})
    <Response [201]>

Create a new document and let CouchDB auto-generate an ``_id`` for it::

    >>> db.insert({'title': 'Ziggy Stardust'})
    <Response [201]>

You can update an existing doc using ``_rev``::

    >>> r = db.get('mydoc')
    >>> result = r.json()
    >>> db.insert({'_id': 'mydoc', '_rev': result['_rev'], 'title': "Let's Dance"})
    <Response [201]>

.. _restrictions on valid property names: http://wiki.apache.org/couchdb/HTTP_Document_API#Special_Fields

Fetch a document
----------------

Retrieves a document, specified by ``_id``::

    >>> db.get('mydoc')
    <Response [200]>

Delete a document
-----------------

Deletes the document::

    >>> r = db.get('mydoc')
    >>> result = r.json()
    >>> db.remove(result['_id'], result['_rev'])
    <Response [200]>

You can also delete a document by using ``insert()`` with
``{'_deleted': True}``::

    >>> r = db.get('mydoc')
    >>> result = r.json()
    >>> result['_deleted'] = True
    >>> db.insert(result)
    <Response [200]>

Create/update a batch of documents
----------------------------------

Create, update or delete multiple documents::

    >>> db.bulk_docs([
            {'_id': 'doc1', 'title': 'Lisa Says'},
            {'_id': 'doc2', 'title': 'Space Oddity'},
        ])
    <Response [201]>

If you omit an ``_id`` parameter on a given document, the database will create
a new document and assign the ID for you::

    >>> db.bulk_docs([
            {'title': 'Lisa Says'},
            {'title': 'Space Oddity'},
        ])
    <Response [201]>

To update a document, you must include both an ``_id`` parameter and a ``_rev``
parameter, which should match the ID and revision of the document on which to
base your updates::

    >>> db.bulk_docs([
            {
                '_id': 'doc1',
                '_rev': '1-84abc2a942007bee7cf55007cba56198',
                'title': 'Lisa Says',
                'artist': 'Velvet Underground',

            },
            {
                '_id': 'doc2',
                '_rev': '1-7b80fc50b6af7a905f368670429a757e',
                'title': 'Space Oddity',
                'artist': 'David Bowie',
            },
        ])
    <Response [201]>

Finally, to delete a document, include a ``_deleted`` parameter with the value
``True``::

    >>> db.bulk_docs([
            {
                '_id': 'doc1',
                '_rev': '1-84abc2a942007bee7cf55007cba56198',
                'title': 'Lisa Says',
                '_deleted': True,

            },
            {
                '_id': 'doc2',
                '_rev': '1-7b80fc50b6af7a905f368670429a757e',
                'title': 'Space Oddity',
                '_deleted': True,
            },
        ])
    <Response [201]>

Fetch a batch of documents
--------------------------

Fetch multiple documents, indexed and sorted by the ``_id``::

    >>> payload = {'include_docs': True, 'attachments': True}
    >>> db.all_docs(params=payload)
    <Response [200]>

You can use ``startkey``/``endkey`` to find all docs in a range::

    >>> payload = {'include_docs': True, 'attachments': True, 'startkey': 'bar', 'endkey': 'quux'}
    >>> db.all_docs(params=payload)
    <Response [200]>

You can also do a prefix search – i.e. "give me all the documents whose ``_id``
start with ``'foo'``" – by using the special high Unicode character
``'\uffff'``::

    >>> payload = {'include_docs': True, 'attachments': True, 'startkey': 'foo', 'endkey': 'foo\uffff'}
    >>> db.all_docs(params=payload)
    <Response [200]>

Save an attachment
------------------

Attaches a binary object to a document.

This method will update an existing document to add the attachment, so it
requires a ``rev`` if the document already exists. If the document doesn't
already exist, then this method will create an empty document containing the
attachment::

    >>> attachment = open('/tmp/att.txt')
    >>> db.insert_att('doc', None, 'att.txt', attachment, 'text/plain')
    <Response [201]>

Get an attachment
-----------------

Get attachment data.

Get an attachment with filename ``'att.txt'`` from document with ID ``'doc'``::

    >>> db.get_att('doc', 'att.txt')
    <Response [200]>

Get an attachment with filename ``'att.txt'`` from document with ID ``'doc'``,
at the revision ``'1-abcd'``::

    >>> payload = {'rev': '1-abcd'}
    >>> db.get_att('doc', 'att.txt', params=payload)

Delete an attachment
--------------------

Delete an attachment from a doc. You must supply the ``rev`` of the existing
doc::

    >>> r = db.get('mydoc')
    >>> result = r.json()
    >>> db.remove_att('doc', result['_rev'], 'att.txt')
    <Response [200]>

Get database information
------------------------

Get information about a database::

    >>> db.info()
    <Response [200]>

Compact the database
--------------------

Triggers a compaction operation in the database. This reduces the database's
size by removing unused and old data, namely non-leaf revisions and attachments
that are no longer referenced by those revisions::

    >>> db.compact()
    <Response [202]>
