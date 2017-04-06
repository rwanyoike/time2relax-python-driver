# time2relax: Python CouchDB Driver

[![Version](https://img.shields.io/pypi/v/time2relax.svg)](https://pypi.python.org/pypi/time2relax)
[![Python](https://img.shields.io/pypi/pyversions/time2relax.svg)](https://pypi.python.org/pypi/time2relax)
[![License](https://img.shields.io/pypi/l/time2relax.svg)](LICENSE)
[![Build](https://img.shields.io/travis/rwanyoike/time2relax.svg)](https://travis-ci.org/rwanyoike/time2relax)
[![Coverage](https://img.shields.io/codecov/c/gh/rwanyoike/time2relax.svg)](https://codecov.io/gh/rwanyoike/time2relax)
[![Docs](https://readthedocs.org/projects/time2relax/badge/?version=latest)](https://readthedocs.org/projects/time2relax/?badge=latest)

> A CouchDB driver for Python.

**time2relax** is a Python [CouchDB](http://couchdb.com/) driver powered by [Requests](https://github.com/kennethreitz/requests#feature-support). It tries to offer a tiny level of abstraction between you, Requests, and CouchDB.

Inspired by [pouchdb](https://github.com/pouchdb/pouchdb) and [nano](https://github.com/dscape/nano) APIs, it features:

- Requests (HTTP for Humans) under the hood
- Transparent URL and parameter encoding
- Exceptions modeled from CouchDB errors

**time2relax** officially supports Python 2.6–2.7 & 3.3–3.5, and works on PyPy.

Tested on CouchDB 1.6.x.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [time2relax.CouchDB(url, skip_setup=False)](#time2relaxcouchdburl-skipsetupfalse)
    - [db.destroy(**kwargs)](#dbdestroykwargs)
    - [db.insert(doc, **kwargs)](#dbinsertdoc-kwargs)
    - [db.get(doc_id, params=None, **kwargs)](#dbgetdocid-paramsnone-kwargs)
    - [db.remove(doc_id, doc_rev, **kwargs)](#dbremovedocid-docrev-kwargs)
    - [db.bulk_docs(docs, json=None, **kwargs)](#dbbulkdocsdocs-jsonnone-kwargs)
    - [db.all_docs(params=None, **kwargs)](#dballdocsparamsnone-kwargs))
    - [db.replicate_to(target, json=None, **kwargs)](#dbreplicatetotarget-jsonnone-kwargs)
    - [db.insert_att(doc_id, doc_rev, att_id, att, att_type, **kwargs)](#dbinsertattdocid-docrev-attid-att-atttype-kwargs)
    - [db.get_att(doc_id, att_id, **kwargs)](#dbgetattdocid-attid-kwargs)
    - [db.remove_att(doc_id, doc_rev, att_id, **kwargs)](#dbremoveattdocid-docrev-attid-kwargs)
    - [db.info(**kwargs)](#dbinfokwargs)
    - [db.compact(**kwargs)](#dbcompactkwargs)
    - [db.ddoc_list(ddoc_id, func_id, view_id, other_id=None, **kwargs)](#dbddoclistddocid-funcid-viewid-otheridnone-kwargs)
    - [db.ddoc_show(ddoc_id, func_id, doc_id=None, **kwargs)](#dbddocshowddocid-funcid-docidnone-kwargs)
    - [db.ddoc_view(ddoc_id, func_id, params=None, **kwargs)](#dbddocviewddocid-funcid-paramsnone-kwargs)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Installation

To install **time2relax**, simply run:

```shell
$ pip install -U time2relax
✨🛋✨
```

## Usage

Detailed documentation is available at [https://time2relax.readthedocs.org](https://time2relax.readthedocs.org).

### time2relax.CouchDB(url, skip_setup=False)

To use **time2relax**, you need to connect it to a CouchDB instance:

```python
>>> from time2relax import CouchDB
>>> db = CouchDB('http://localhost:5984/dbname')
```

Most of the API is exposed as:

```python
>>> db.function(*args, **kwargs)
```

Where `**kwargs` are optional arguments that `requests.Request` can take.

Initially **time2relax** will check if the database exists, or try to create it. `skip_setup=True` disables this behavior:

```python
>>> db = CouchDB('http://localhost:5984/dbname', skip_setup=True)
```

#### db.destroy(**kwargs)

Delete the database:

```python
>>> db.destroy()
<Response [200]>
```

#### db.insert(doc, **kwargs)

Create or update an existing document:

```python
>>> db.insert({'_id': 'docid', 'title': 'Heros'})
<Response [201]>
```

#### db.get(doc_id, params=None, **kwargs)

Retrieve a document:

```python
>>> db.get('docid')
<Response [200]>
```

#### db.remove(doc_id, doc_rev, **kwargs)

Delete a document:

```python
>>> db.remove('docid', 'revid')
<Response [200]>
```

#### db.bulk_docs(docs, json=None, **kwargs)

Create, update or delete multiple documents:

```python
>>> db.bulk_docs([
...     {'_id': 'doc1', 'title': 'Lisa Says'},
...     {'_id': 'doc2', 'title': 'Space Oddity'},
... ])
<Response [201]>
```

#### db.all_docs(params=None, **kwargs)

Fetch multiple documents:

```python
>>> db.all_docs({'include_docs': True, 'attachments': True})
<Response [200]>
```

#### db.replicate_to(target, json=None, **kwargs)

Replicate data from source (`db`) to target:

```python
>>> db.replicate_to('http://localhost:5984/otherdb')
<Response [200]>
```

#### db.insert_att(doc_id, doc_rev, att_id, att, att_type, **kwargs)

Create or update an existing attachment:

```python
>>> with open('/tmp/att.txt') as att:
...     db.insert_att('docid', None, 'att.txt', att, 'text/plain')
...
<Response [201]>
```

#### db.get_att(doc_id, att_id, **kwargs)

Retrieve an attachment:

```python
>>> db.get_att('docid', 'att.txt')
<Response [200]>
```

#### db.remove_att(doc_id, doc_rev, att_id, **kwargs)

Delete an attachment:

```python
>>> db.remove_att('docid', 'revid', 'att.txt')
<Response [200]>
```

#### db.info(**kwargs):

Get information about the database:

```python
>>> db.info()
<Response [200]>
```

#### db.compact(**kwargs):

Trigger a compaction operation:

```python
>>> db.compact()
<Response [202]>
```

#### db.ddoc_list(ddoc_id, func_id, view_id, other_id=None, **kwargs)

Apply a list function against a view:

```python
>>> db.ddoc_list('testid', 'listid', 'viewid')
<Response [200]>
```

#### db.ddoc_show(ddoc_id, func_id, doc_id=None, **kwargs)

Apply a show function against a document:

```python
>>> db.ddoc_show('testid', 'showid')
<Response [200]>
```

#### db.ddoc_view(ddoc_id, func_id, params=None, **kwargs)

Execute a view function:

```python
>>> db.ddoc_view('testid', 'viewid', {'reduce': False, 'key': 'key2'})
<Response [200]>
```

## Maintainers

- [@rwanyoike](https://github.com/rwanyoike)

## Contribute

Feel free to [dive in](https://time2relax.readthedocs.io/en/latest/contributing.html), open an issue or submit a PR.

**time2relax** follows the [Contributor Covenant](CODE_OF_CONDUCT.md) code of conduct.

## License

[MIT](LICENSE) © Raymond Wanyoike
