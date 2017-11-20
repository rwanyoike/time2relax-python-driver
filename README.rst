time2relax: Python CouchDB Driver
=================================

.. image:: https://img.shields.io/pypi/v/time2relax.svg
   :target: https://pypi.python.org/pypi/time2relax

.. image:: https://img.shields.io/pypi/l/time2relax.svg
   :target: https://pypi.python.org/pypi/time2relax

.. image:: https://img.shields.io/pypi/pyversions/time2relax.svg
   :target: https://pypi.python.org/pypi/time2relax

.. image:: https://img.shields.io/travis/rwanyoike/time2relax.svg
   :target: https://travis-ci.org/rwanyoike/time2relax

.. image:: https://img.shields.io/codecov/c/gh/rwanyoike/time2relax.svg
   :target: https://codecov.io/gh/rwanyoike/time2relax

..

    A CouchDB driver for Python.

time2relax is a Python `CouchDB`_ driver that tries to offer a minimal level of
abstraction between you and CouchDB.

To use time2relax:

.. code-block:: python

    >>> from time2relax import CouchDB
    >>> db = CouchDB('http://localhost:5984/dbname')
    >>> db.insert({'title': 'Ziggy Stardust'})
    <Response [201]>

.. _CouchDB: https://couchdb.apache.org/

Feature Support
---------------

Inspired by `pouchdb`_ and `couchdb-nano`_ APIs, it features:

* `Requests`_ ✨🍰✨ (HTTP for Humans) under the hood.
* Transparent URL and `parameter encoding`_.
* HTTP exceptions modelled from CouchDB `error codes`_.
* Tested on CouchDB 1.6.x and 1.7.x (2.x.x *unknown*).

time2relax officially supports **Python 2.7, 3.3+, and PyPy**.

.. _pouchdb: https://github.com/pouchdb/pouchdb
.. _couchdb-nano: https://github.com/apache/couchdb-nano
.. _Requests: https://requests.readthedocs.io/en/latest
.. _parameter encoding: https://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
.. _error codes: http://docs.couchdb.org/en/1.6.1/api/basics.html#http-status-codes

Installation
------------

To install time2relax, simply run:

.. code-block:: shell

    $ pip install -U time2relax
    ✨🛋✨

Documentation
-------------

Detailed documentation is available at https://time2relax.readthedocs.org.

How to Contribute
-----------------

#. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the
   **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as
   expected.
#. Send a pull request and bug the maintainer until it gets merged and
   published. :) Make sure to add yourself to AUTHORS_.

time2relax follows the `Contributor Covenant`_ code of conduct.

.. _`the repository`: http://github.com/rwanyoike/time2relax
.. _AUTHORS: https://github.com/rwanyoike/time2relax/blob/master/AUTHORS.rst
.. _Contributor Covenant: https://github.com/rwanyoike/time2relax/blob/master/CODE_OF_CONDUCT.md
