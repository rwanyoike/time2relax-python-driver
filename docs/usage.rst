=====
Usage
=====

To use time2relax in a project::

    import time2relax

Server functions
----------------

Representation of a CouchDB server:

.. code:: python

    from time2relax import Server

    couchdb = Server()

server.auth(username, password)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

time2relax supports making requests using CouchDB's cookie authentication:

.. code:: python

    couchdb.auth('admin', 'hackme')

Getting the cookie:

.. code:: python

    auth = couchdb.client.session.cookies['AuthSession']

Reusing a cookie:

.. code:: python

    couchdb.client.session.cookies['AuthSession'] = auth

Getting the current session:

.. code:: python

    r = couchdb.session()
    session = r.json()

    print 'User is {0} and has these roles {1}'.format(
        session['userCtx']['name'], session['userCtx']['roles'])

server.compact(name, ddoc=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compacts a CouchDB database, ``name``, if ``ddoc`` is specified also compacts its views:

.. code:: python

    couchdb.compact('alice')

server.create(name)
~~~~~~~~~~~~~~~~~~~

Creates a CouchDB database with the given ``name``:

.. code:: python

    couchdb.create('alice')

    # No exception thrown
    print 'Database alice created!'

server.delete(name)
~~~~~~~~~~~~~~~~~~~

Deletes a CouchDB database with the given ``name``:

.. code:: python

    couchdb.delete('alice')

server.get(name)
~~~~~~~~~~~~~~~~

Get information about a CouchDB database, ``name``:

.. code:: python

    r = couchdb.get('alice')
    info = r.json()

    print info

server.list(name)
~~~~~~~~~~~~~~~~~

Lists all the databases in CouchDB:

.. code:: python

    r = couchdb.list()

    # Body is an array
    for i in r.json():
        print i

server.replicate(name, target, options=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replicates a CouchDB database, ``name``, on ``target`` with options ``options``. ``target`` has to exist, add ``create_target: True`` to ``options`` to create it prior to replication.

.. code:: python

    target = 'http://admin:hackme@otherhost.com:5984/alice'
    couchdb.replicate('alice', target, {'create_target': True})

Database functions
------------------

Representation of a CouchDB database:

.. code:: python

    from time2relax import Server, Database

    couchdb = Server()
    db = Database(couchdb, 'alice')

db.insert(doc, params=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* TODO

db.delete(_id, rev)
~~~~~~~~~~~~~~~~~~~

* TODO

db.get(_id, params=None)
~~~~~~~~~~~~~~~~~~~~~~~~

* TODO

db.head(_id)
~~~~~~~~~~~~

* TODO

db.bulk(docs, options=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* TODO

db.list(params=None)
~~~~~~~~~~~~~~~~~~~~

* TODO
