time2relax - A CouchDB driver
=============================

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

* Free software: MIT license
* Documentation: https://time2relax.readthedocs.org.

.. _CouchDB: http://couchdb.com/

Features
--------

* Runs `python-requests`_ under the hood ⚡️.
* Only a minimum of abstraction between you and CouchDB.
* Errors are proxied directly from CouchDB: if you know CouchDB you already
  know `time2relax`.
* Python 2.6–2.7 & 3.3–3.5 support.
* Transparent URL and parameter encoding.

.. _python-requests: http://requests.readthedocs.io/en/latest/#supported-features
