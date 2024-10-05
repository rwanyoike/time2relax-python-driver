# time2relax: Python CouchDB Driver

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/rwanyoike/time2relax-python-driver/python-package.yml?branch=main)
](https://github.com/rwanyoike/time2relax-python-driver/actions/workflows/python-package.yml?query=branch%3Amain)
[![GitHub License](https://img.shields.io/github/license/rwanyoike/time2relax-python-driver)
](LICENSE.txt)
[![PyPI - Version](https://img.shields.io/pypi/v/time2relax)
](https://pypi.org/project/time2relax)

> A CouchDB driver for Python.

time2relax is a Python [CouchDB](https://couchdb.apache.org/) driver that tries to offer a _minimal level of abstraction_ between you and CouchDB.

Basic insert usage:

```python
>>> from time2relax import CouchDB
>>> db = CouchDB('http://localhost:5984/dbname')
>>> db.insert({'title': 'Ziggy Stardust'})
<Response [201]>
```

[Features](#features) | [Installation](#installation) | [Usage](#usage) | [Contributing](#contributing) | [License](#license) | [Related Projects](#related-projects)

## Features

Inspired by [pouchdb](https://github.com/pouchdb/pouchdb)  and [couchdb-nano](https://github.com/apache/couchdb-nano) APIs, it features:

- [Requests](https://requests.readthedocs.io/en/latest) (HTTP for Humans) under the hood.
- HTTP exceptions modeled from CouchDB [error codes](http://docs.couchdb.org/en/1.6.1/api/basics.html#http-status-codes).
- Transparent URL and parameter encoding.

time2relax officially supports Python 3.8+; CouchDB 1.7+.

## Installation

To install time2relax, simply run:

```shell
$ pip install -U time2relax
✨🛋✨
```

## Usage

For documentation, see [`./docs/README.md`](./docs/README.md).
