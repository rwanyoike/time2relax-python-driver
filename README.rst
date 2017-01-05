time2relax - Python CouchDB driver
==================================

.. image:: https://img.shields.io/pypi/v/time2relax.svg
        :target: https://pypi.python.org/pypi/time2relax
.. image:: https://img.shields.io/travis/rwanyoike/time2relax.svg
        :target: https://travis-ci.org/rwanyoike/time2relax
.. image:: https://img.shields.io/codecov/c/gh/rwanyoike/time2relax.svg
        :target: https://codecov.io/gh/rwanyoike/time2relax
.. image:: https://readthedocs.org/projects/time2relax/badge/?version=latest
        :target: https://readthedocs.org/projects/time2relax/?badge=latest
        :alt: Documentation Status

A `CouchDB`_ driver for Python.

* Documentation: https://time2relax.readthedocs.org.
* Free software: MIT license

.. _CouchDB: http://couchdb.com/

Features
--------

* Runs `python-requests`_ under the hood.
* Only a minimum level of abstraction between you and CouchDB.
* Transparent URL and parameter encoding.
* Exceptions are modelled from CouchDB errors.
* Python 2.6–2.7 & 3.3–3.5 support.
* Tested with CouchDB 1.6.x (2.0 pending)

Inspired by `pouchdb`_ and `nano`_ APIs.

.. _python-requests: http://requests.readthedocs.io/en/latest/#supported-features
.. _pouchdb: https://github.com/pouchdb/pouchdb
.. _nano: https://github.com/dscape/nano

Quickstart
----------

Install the latest time2relax if you haven't yet:

.. code:: shell

    $ pip install -U time2relax

To use time2relax in a project:

.. code:: python

    >>> from time2relax import CouchDB
    >>> db = CouchDB('http://localhost:5984/dbname')

Then:

.. code:: python

    >>> db.insert({'title': 'Ziggy Stardust'})
    <Response [201]>
