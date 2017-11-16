Usage
=====

To use time2relax in a project::

    >>> from time2relax import CouchDB
    >>> db = CouchDB('http://localhost:5984/dbname')

Most of the API is exposed as::

    >>> db.function(*args, **kwargs)

Where ``**kwargs`` are optional arguments that :class:`requests.Request` takes.

Create a database
-----------------

Initially the ``CouchDB`` object will check if the database exists, and try to
create it if it does not. You can use ``create_database=False`` to skip this setup::

    >>> db = CouchDB('http://localhost:5984/dbname', create_database=False)

Delete a database
-----------------

Delete the database::

    >>> db.destroy()
    <Response [200]>

Further requests with the ``CouchDB`` object will raise a
:class:`time2relax.CouchDBError`::

    >>> db.info()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "time2relax/__init__.py", line 243, in info
        return self.request('GET', **kwargs)
      File "time2relax/__init__.py", line 371, in request
        raise CouchDBError('Database is destroyed')
    time2relax.CouchDBError: Database is destroyed

Create/update a document
------------------------

Note: There are some `restrictions on valid property names`_ of the documents.

Create a new document::

    >>> db.insert({'_id': 'docid', 'title': 'Heros'})
    <Response [201]>

To create a new document and let CouchDB auto-generate an ``_id`` for it::

    >>> db.insert({'title': 'Ziggy Stardust'})
    <Response [201]>

If the document already exists, you must specify its revision ``_rev``,
otherwise a conflict will occur. You can update an existing document using
``_rev``::

    >>> r = db.get('docid')
    >>> result = r.json()
    >>> db.insert({'_id': result['_id'], '_rev': result['_rev'], 'title': 'Dance'})
    <Response [201]>

.. _restrictions on valid property names: http://wiki.apache.org/couchdb/HTTP_Document_API#Special_Fields

Fetch a document
----------------

Retrieve a document::

    >>> db.get('docid')
    <Response [200]>

Delete a document
-----------------

You must supply the ``_rev`` of the existing document.

Delete a document::

    >>> r = db.get('docid')
    >>> result = r.json()
    >>> db.remove(result['_id'], result['_rev'])
    <Response [200]>

You can also delete a document by using :meth:`time2relax.CouchDB.insert` with
``{'_deleted': True}``::

    >>> r = db.get('docid')
    >>> result = r.json()
    >>> result['_deleted'] = True
    >>> db.insert(result)
    <Response [200]>

Create/update a batch of documents
----------------------------------

Create multiple documents::

    >>> db.bulk_docs([
    ...     {'_id': 'doc1', 'title': 'Lisa Says'},
    ...     {'_id': 'doc2', 'title': 'Space Oddity'},
    ... ])
    <Response [201]>

If you omit an ``_id`` parameter on a given document, the database will create
a new document and assign the ID for you::

    >>> db.bulk_docs([
    ...     {'title': 'Lisa Says'},
    ...     {'title': 'Space Oddity'},
    ... ])
    <Response [201]>

To update a document, you must include both an ``_id`` parameter and a ``_rev``
parameter, which should match the ID and revision of the document on which to
base your updates::

    >>> db.bulk_docs([
    ...     {
    ...         '_id': 'doc1',
    ...         '_rev': '1-84abc2a942007bee7cf55007cba56198',
    ...         'title': 'Lisa Says',
    ...         'artist': 'Velvet Underground',
    ...     },
    ...     {
    ...         '_id': 'doc2',
    ...         '_rev': '1-7b80fc50b6af7a905f368670429a757e',
    ...         'title': 'Space Oddity',
    ...         'artist': 'David Bowie',
    ...     },
    ... ])
    <Response [201]>

Finally, to delete a document, include a ``_deleted`` parameter with the value
``True``::

    >>> db.bulk_docs([
    ...     {
    ...         '_id': 'doc1',
    ...         '_rev': '1-84abc2a942007bee7cf55007cba56198',
    ...         'title': 'Lisa Says',
    ...         '_deleted': True,
    ...     },
    ...     {
    ...         '_id': 'doc2',
    ...         '_rev': '1-7b80fc50b6af7a905f368670429a757e',
    ...         'title': 'Space Oddity',
    ...         '_deleted': True,
    ...     },
    ... ])
    <Response [201]>

Fetch a batch of documents
--------------------------

Fetch multiple documents::

    >>> params = {'include_docs': True, 'attachments': True}
    >>> db.all_docs(params=params)
    <Response [200]>

You can use ``startkey``/``endkey`` to find all docs in a range::

    >>> params = {'include_docs': True, 'attachments': True, 'startkey': 'bar', 'endkey': 'quux'}
    >>> db.all_docs(params=params)
    <Response [200]>

You can also do a prefix search – i.e. "give me all the documents whose ``_id``
start with ``'foo'``" – by using the special high Unicode character
``'\uffff'``::

    >>> params = {'include_docs': True, 'attachments': True, 'startkey': 'foo', 'endkey': 'foo\uffff'}
    >>> db.all_docs(params=params)
    <Response [200]>

Replicate a database
--------------------

Replicate the database to a target::

    >>> db.replicate_to('http://localhost:5984/otherdb')
    <Response [200]>

The target has to exist, add ``json={'create_target': True}`` to create it
prior to replication.

Save an attachment
------------------

This method will update an existing document to add the attachment, so it
requires a ``_rev`` if the document already exists. If the document doesn't
already exist, then this method will create an empty document containing the
attachment.

Attach a binary object::

    >>> with open('/tmp/att.txt') as att:
    ...     db.insert_att('docid', None, 'att.txt', att, 'text/plain')
    ...
    <Response [201]>

Get an attachment
-----------------

Get attachment data::

    >>> db.get_att('docid', 'att.txt')
    <Response [200]>

Delete an attachment
--------------------

You must supply the ``_rev`` of the existing document.

Delete an attachment::

    >>> r = db.get('docid')
    >>> result = r.json()
    >>> db.remove_att(result['_id'], result['_rev'], 'att.txt')
    <Response [200]>

Get database information
------------------------

Get information about the database::

    >>> db.info()
    <Response [200]>

Compact the database
--------------------

This reduces the database's size by removing unused and old data, namely
non-leaf revisions and attachments that are no longer referenced by those
revisions.

Trigger a compaction operation::

    >>> db.compact()
    <Response [202]>

Run a list function
-------------------

Make sure you understand how list functions work in CouchDB. A good start is
`the CouchDB guide entry on lists`_::

    >>> db.insert({
    ...     '_id': '_design/testid',
    ...     'views': {
    ...         'viewid': {
    ...             'map': "function (doc) {"
    ...                    "    emit(doc._id, 'value');"
    ...                    "}",
    ...         },
    ...     },
    ...     'lists': {
    ...         'listid': "function (head, req) {"
    ...                   "    return 'Hello World!';"
    ...                   "}",
    ...     },
    ... })
    <Response [201]>
    >>> db.ddoc_list('testid', 'listid', 'viewid')
    <Response [200]>

.. _the CouchDB guide entry on lists: http://guide.couchdb.org/draft/transforming.html

Run a show function
-------------------

Make sure you understand how show functions work in CouchDB. A good start is
`the CouchDB guide entry on shows`_::

    >>> db.insert({
    ...     '_id': '_design/testid',
    ...     'shows': {
    ...         'showid': "function (doc, req) {"
    ...                   "    return {body: 'relax!'}"
    ...                   "}",
    ...     },
    ... })
    <Response [201]>
    >>> db.ddoc_show('testid', 'showid')
    <Response [200]>

.. _the CouchDB guide entry on shows: http://guide.couchdb.org/draft/show.html

Run a view function
-------------------

Make sure you understand how view functions work in CouchDB. A good start is
`the CouchDB guide entry on views`_::

    >>> db.insert({
    ...     '_id': '_design/testid',
    ...     'views': {
    ...         'viewid': {
    ...             'map': "function (doc) {"
    ...                    "    emit(doc.key);"
    ...                    "}",
    ...         },
    ...     },
    ... })
    <Response [201]>
    >>> params = {'reduce': False, 'key': 'key2'}
    >>> db.ddoc_view('testid', 'viewid', params=params)
    <Response [200]>

.. _the CouchDB guide entry on views: http://guide.couchdb.org/draft/views.html
