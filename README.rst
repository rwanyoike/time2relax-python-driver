==========
time2relax
==========

.. image:: https://img.shields.io/pypi/v/time2relax.svg
        :target: https://pypi.python.org/pypi/time2relax

.. image:: https://img.shields.io/travis/rwanyoike/time2relax.svg
        :target: https://travis-ci.org/rwanyoike/time2relax

.. image:: https://img.shields.io/codecov/c/gh/rwanyoike/time2relax.svg
        :target: https://codecov.io/gh/rwanyoike/time2relax

.. image:: https://readthedocs.org/projects/time2relax/badge/?version=latest
        :target: https://readthedocs.org/projects/time2relax/?badge=latest
        :alt: Documentation Status

A CouchDB driver for Python.

.. code:: python

    >>> import time2relax
    >>> db = time2relax.CouchDB('http://localhost:5984/dbname')
    >>> db.info()
    <Response [200]>

* Free software: MIT license
* Documentation: https://time2relax.readthedocs.org.

Features
--------

* Uses `python-requests`_ ☺.

.. _python-requests: http://docs.python-requests.org/en/latest/
