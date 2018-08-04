# time2relax: Python CouchDB Driver

[![Travis (.org)](https://img.shields.io/travis/rwanyoike/time2relax.svg)](https://travis-ci.org/rwanyoike/time2relax)
[![Codecov](https://img.shields.io/codecov/c/gh/rwanyoike/time2relax.svg)](https://codecov.io/gh/rwanyoike/time2relax)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/time2relax.svg)](https://pypi.python.org/pypi/time2relax)
[![PyPI - License](https://img.shields.io/pypi/l/time2relax.svg)](https://pypi.python.org/pypi/time2relax)

> A CouchDB driver for Python.

time2relax is a Python [CouchDB](https://couchdb.apache.org/) driver that tries to offer a minimal level of abstraction between you and CouchDB.

Basic insert usage:

```python
>>> from time2relax import CouchDB
>>> db = CouchDB('http://localhost:5984/dbname')
>>> db.insert({'title': 'Ziggy Stardust'})
<Response [201]>
```

<details>
<summary>Table of Contents</summary>

- [Feature Support](#feature-support)
- [Installation](#installation)
- [Documentation](#documentation)
  - [Create a Database](#create-a-database)
  - [Delete a Database](#delete-a-database)
  - [Create/Update a Document](#createupdate-a-document)
  - [Fetch a Document](#fetch-a-document)
  - [Delete a Document](#delete-a-document)
  - [Create/Update a Batch of Documents](#createupdate-a-batch-of-documents)
  - [Fetch a Batch of Documents](#fetch-a-batch-of-documents)
  - [Replicate a Database](#replicate-a-database)
  - [Save an Attachment](#save-an-attachment)
  - [Get an Attachment](#get-an-attachment)
  - [Delete an Attachment](#delete-an-attachment)
  - [Get Database Information](#get-database-information)
  - [Compact a Database](#compact-a-database)
  - [Run a List Function](#run-a-list-function)
  - [Run a Show Function](#run-a-show-function)
  - [Run a View Function](#run-a-view-function)
- [How to Contribute](#how-to-contribute)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>
</details>

## Feature Support

Inspired by [pouchdb](https://github.com/pouchdb/pouchdb)  and [couchdb-nano](https://github.com/apache/couchdb-nano) APIs, it features:

* [Requests](https://requests.readthedocs.io/en/latest) (HTTP for Humans) under the hood.
* Transparent URL and parameter encoding.
* HTTP exceptions modeled from CouchDB [error codes](http://docs.couchdb.org/en/1.6.1/api/basics.html#http-status-codes).
* Support for CouchDB 1.7.x.

time2relax officially supports **Python 2.7 and 3.6+**.

## Installation

To install time2relax, simply run:

```
$ pip install -U time2relax
✨🛋✨
```

## Documentation

[![Read the Docs](https://img.shields.io/readthedocs/time2relax.svg)](https://time2relax.readthedocs.org)

Detailed documentation is available at [https://time2relax.readthedocs.org](https://time2relax.readthedocs.org).

---

To use time2relax in a project:

```python
>>> from time2relax import CouchDB
>>> db = CouchDB('http://localhost:5984/dbname')
```

Most of the API is exposed as `db.FUNCTION(*args, **kwargs)`, where `**kwargs` are optional arguments that `requests.Session.request` can take.

### Create a Database

Initially the `CouchDB` object will check if the database exists, and try to create it if it does not. You can use `create_db=False` to skip this step:

```python
>>> db = CouchDB('http://localhost:5984/dbname', create_db=False)
```

### Delete a Database

Delete a database:

```python
>>> db.destroy()
<Response [200]>
```

Further requests with the `CouchDB` object should raise a `time2relax.ResourceNotFound`:

```python
>>> db.info()
ResourceNotFound: ({'error': 'not_found', 'reason': 'missing'}, <Response [404]>)
```

### Create/Update a Document

Note: There are some CouchDB restrictions on valid property names of the documents.

Create a new document:

```python
>>> db.insert({'_id': 'docid', 'title': 'Heros'})
<Response [201]>
```

To create a new document and let CouchDB auto-generate an `_id` for it:

```python
>>> db.insert({'title': 'Ziggy Stardust'})
<Response [201]>
```

If the document already exists, you must specify its revision `_rev`, otherwise a conflict will occur. You can update an existing document using `_rev`:

```python
>>> result = db.get('docid').json()
>>> db.insert({'_id': result['_id'], '_rev': result['_rev'], 'title': 'Dance'})
<Response [201]>
```

### Fetch a Document

Retrieve a document:

```python
>>> db.get('docid')
<Response [200]>
```

### Delete a Document

You must supply the `_rev` of the existing document.

Delete a document:

```python
>>> result = db.get('docid').json()
>>> db.remove(result['_id'], result['_rev'])
<Response [200]>
```

You can also delete a document by using `time2relax.CouchDB.insert` with `{'_deleted': True}`:

```python
>>> result = db.get('docid').json()
>>> result['_deleted'] = True
>>> db.insert(result)
<Response [200]>
```

### Create/Update a Batch of Documents

Create multiple documents:

```python
>>> db.bulk_docs([
...     {'_id': 'doc1', 'title': 'Lisa Says'},
...     {'_id': 'doc2', 'title': 'Space Oddity'},
... ])
<Response [201]>
```

If you omit the `_id` parameter on a given document, the database will create a new document and assign the ID for you:

```python
>>> db.bulk_docs([
...     {'title': 'Lisa Says'},
...     {'title': 'Space Oddity'},
... ])
<Response [201]>
```

To update a document, you must include both an `_id` parameter and a `_rev` parameter, which should match the ID and revision of the document on which to base your updates:

```python
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
```

Finally, to delete a document, include a `_deleted` parameter with the value `True`:

```python
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
```

### Fetch a Batch of Documents

Fetch multiple documents:

```python
>>> params = {'include_docs': True, 'attachments': True}
>>> db.all_docs(params)
<Response [200]>
```

You can use `startkey`/`endkey` to find all docs in a range:

```python
>>> params = {'startkey': 'bar', 'endkey': 'quux'}
>>> db.all_docs(params)
<Response [200]>
```

You can also do a prefix search – i.e. "give me all the documents whose `_id` start with `'foo'`" – by using the special high Unicode character `'\uffff'`:

```python
>>> params = {'startkey': 'foo', 'endkey': 'foo\uffff'}
>>> db.all_docs(params)
<Response [200]>
```

### Replicate a Database

Note: The target has to exist, you can use `json={'create_target': True}` to create it prior to replication.

Replicate a database to a target:

```python
>>> db.replicate_to('http://localhost:5984/otherdb')
<Response [200]>
```

### Save an Attachment

This method will update an existing document to add an attachment, so it requires a `_rev` if the document already exists. If the document doesn't already exist, then this method will create an empty document containing the attachment.

Attach a text/plain file:

```python
>>> with open('/tmp/att.txt') as fp:
...     db.insert_att('docid', None, 'att.txt', fp, 'text/plain')
...
<Response [201]>
```

### Get an Attachment

Get attachment data:

```python
>>> db.get_att('docid', 'att.txt')
<Response [200]>
```

### Delete an Attachment

You must supply the `_rev` of the existing document.

Delete an attachment:

```python
>>> result = db.get('docid').json()
>>> db.remove_att(result['_id'], result['_rev'], 'att.txt')
<Response [200]>
```

### Get Database Information

Get information about a database:

```python
>>> db.info()
<Response [200]>
```

### Compact a Database

This reduces a database's size by removing unused and old data, namely non-leaf revisions and attachments that are no longer referenced by those revisions.

Trigger a compaction operation:

```python
>>> db.compact()
<Response [202]>
```

### Run a List Function

Make sure you understand how list functions work in CouchDB. A good start is [the CouchDB guide entry on lists](http://guide.couchdb.org/draft/transforming.html):

```python
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
```

### Run a Show Function

Make sure you understand how show functions work in CouchDB. A good start is [the CouchDB guide entry on shows](http://guide.couchdb.org/draft/show.html):

```python
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
```

### Run a View Function

Make sure you understand how view functions work in CouchDB. A good start is [the CouchDB guide entry on views](http://guide.couchdb.org/draft/views.html):

```python
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
```

## How to Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
1. Fork [the repository](https://github.com/rwanyoike/time2relax) to start making your changes to the master branch (or branch off of it).
1. Write a test which shows that the bug was fixed or that the feature works as expected.
1. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to [AUTHORS](https://github.com/rwanyoike/time2relax/blob/master/AUTHORS.md).
