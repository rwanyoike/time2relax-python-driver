Usage
=====

To use time2relax in a project::

    >>> from time2relax import CouchDB
    >>> db = CouchDB('http://localhost:5984/dbname')

Create a Database
-----------------

Initially the ``CouchDB`` object will check if the database exists, and try to
create it if it does not. You can use ``create_db=False`` to skip this setup::

    >>> db = CouchDB('http://localhost:5984/dbname', create_db=False)

Delete a Database
-----------------

Delete a database::

    >>> db.destroy()
    <Response [200]>

Further requests with the ``CouchDB`` object should raise a
:class:`time2relax.ResourceNotFound`::

    >>> db.info()
    ResourceNotFound: ({'error': 'not_found', 'reason': 'missing'}, <Response [404]>)

Create/Update a Document
------------------------

Note: There are some CouchDB `restrictions on valid property names`_ of the
documents.

Create a new document::

    >>> db.insert({'_id': 'docid', 'title': 'Heros'})
    <Response [201]>

To create a new document and let CouchDB auto-generate an ``_id`` for it::

    >>> db.insert({'title': 'Ziggy Stardust'})
    <Response [201]>

If the document already exists, you must specify its revision ``_rev``,
otherwise a conflict will occur. You can update an existing document using
``_rev``::

    >>> result = db.get('docid').json()
    >>> db.insert({'_id': result['_id'], '_rev': result['_rev'], 'title': 'Dance'})
    <Response [201]>

.. _restrictions on valid property names: http://wiki.apache.org/couchdb/HTTP_Document_API#Special_Fields

Fetch a Document
----------------

Retrieve a document::

    >>> db.get('docid')
    <Response [200]>

Delete a Document
-----------------

You must supply the ``_rev`` of the existing document.

Delete a document::

    >>> result = db.get('docid').json()
    >>> db.remove(result['_id'], result['_rev'])
    <Response [200]>

You can also delete a document by using :meth:`time2relax.CouchDB.insert` with
``{'_deleted': True}``::

    >>> result = db.get('docid').json()
    >>> result['_deleted'] = True
    >>> db.insert(result)
    <Response [200]>

Create/Update a Batch of Documents
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

Fetch a Batch of Documents
--------------------------

Fetch multiple documents::

    >>> params = {'include_docs': True, 'attachments': True}
    >>> db.all_docs(params)
    <Response [200]>

You can use ``startkey``/``endkey`` to find all docs in a range::

    >>> params = {'startkey': 'bar', 'endkey': 'quux'}
    >>> db.all_docs(params)
    <Response [200]>

You can also do a prefix search – i.e. "give me all the documents whose ``_id``
start with ``'foo'``" – by using the special high Unicode character
``'\uffff'``::

    >>> params = {'startkey': 'foo', 'endkey': 'foo\uffff'}
    >>> db.all_docs(params)
    <Response [200]>

Replicate a Database
--------------------

Note: The target has to exist, you can use ``json={'create_target': True}`` to
create it prior to replication.

Replicate a database to a target::

    >>> db.replicate_to('http://localhost:5984/otherdb')
    <Response [200]>

Save an Attachment
------------------

This method will update an existing document to add an attachment, so it
requires a ``_rev`` if the document already exists. If the document doesn't
already exist, then this method will create an empty document containing the
attachment.

Attach a binary object::

    >>> with open('/tmp/att.txt') as fp:
    ...     db.insert_att('docid', None, 'att.txt', fp, 'text/plain')
    ...
    <Response [201]>

Get an Attachment
-----------------

Get attachment data::

    >>> db.get_att('docid', 'att.txt')
    <Response [200]>

Delete an Attachment
--------------------

You must supply the ``_rev`` of the existing document.

Delete an attachment::

    >>> result = db.get('docid').json()
    >>> db.remove_att(result['_id'], result['_rev'], 'att.txt')
    <Response [200]>

Get Database Information
------------------------

Get information about a database::

    >>> db.info()
    <Response [200]>

Compact a Database
------------------

This reduces a database's size by removing unused and old data, namely non-leaf
revisions and attachments that are no longer referenced by those revisions.

Trigger a compaction operation::

    >>> db.compact()
    <Response [202]>

Run a List Function
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

Run a Show Function
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

Run a View Function
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
    >>> db.ddoc_view('testid', 'viewid', params)
    <Response [200]>

.. _the CouchDB guide entry on views: http://guide.couchdb.org/draft/views.html
