.. time2relax documentation master file, created by sphinx-quickstart on Mon
   Nov 20 22:39:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

time2relax: Python CouchDB Driver
=================================

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://img.shields.io/pypi/l/time2relax.svg
   :target: https://pypi.python.org/pypi/time2relax

.. image:: https://img.shields.io/pypi/wheel/time2relax.svg
   :target: https://pypi.python.org/pypi/time2relax

.. image:: https://img.shields.io/pypi/pyversions/time2relax.svg
   :target: https://pypi.python.org/pypi/time2relax

.. image:: https://img.shields.io/travis/rwanyoike/time2relax.svg
   :target: https://travis-ci.org/rwanyoike/time2relax

.. image:: https://img.shields.io/codecov/c/gh/rwanyoike/time2relax.svg
   :target: https://codecov.io/gh/rwanyoike/time2relax

.. include:: alpha.rst

----

To use time2relax in a project::

    >>> from time2relax import CouchDB
    >>> db = CouchDB('http://localhost:5984/dbname')

Most of the API is exposed as::

    >>> db.function(*args, **kwargs)

Where ``**kwargs`` are optional arguments that :meth:`requests.Session.request`
takes.

Feature Support
---------------

* `Requests`_ ✨🍰✨ (HTTP for Humans) under the hood.
* A minimum level of abstraction between you and CouchDB.
* Transparent URL and `parameter encoding`_.
* HTTP exceptions modeled from CouchDB `error codes`_.
* Support for CouchDB 1.7.x (`tested in CI`_).

time2relax officially supports **Python 2.7, 3.3+, and PyPy**.

.. _Requests: https://requests.readthedocs.io/en/latest
.. _parameter encoding: https://wiki.apache.org/couchdb/HTTP_view_API#Querying_Options
.. _error codes: http://docs.couchdb.org/en/1.6.1/api/basics.html#http-status-codes
.. _tested in CI: https://travis-ci.org/rwanyoike/time2relax

User Guide
----------

.. toctree::
   :maxdepth: 2

   installation
   usage

Community Guide
---------------

.. toctree::
   :maxdepth: 2

   updates

API Guide
---------

.. toctree::
   :maxdepth: 2

   api

Contributor Guide
-----------------

.. toctree::
   :maxdepth: 2

   contributing
   authors
