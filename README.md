# time2relax: Python CouchDB Driver

[![Travis (.org)](https://img.shields.io/travis/rwanyoike/time2relax.svg)](https://travis-ci.org/rwanyoike/time2relax)
[![Codecov](https://img.shields.io/codecov/c/gh/rwanyoike/time2relax.svg)](https://codecov.io/gh/rwanyoike/time2relax)
[![GitHub](https://img.shields.io/github/license/rwanyoike/time2relax)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/time2relax.svg)](https://pypi.python.org/pypi/time2relax)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

time2relax officially supports Python 3.6+; CouchDB 1.7+.

## Installation

To install time2relax, simply run:

```shell
$ pip install -U time2relax
✨🛋✨
```

## Usage

For documentation, see [`./docs/README.md`](./docs/README.md).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](./LICENSE).

## Related Projects

- [couchutils](https://github.com/rwanyoike/couchutils) - A collection of CouchDB utils.
