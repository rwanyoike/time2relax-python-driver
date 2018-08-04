Developer Interface
===================

Main Interface
--------------

.. autoclass:: time2relax.CouchDB
   :inherited-members:

Exceptions
----------

.. autoexception:: time2relax.BadRequest
.. autoexception:: time2relax.Forbidden
.. autoexception:: time2relax.MethodNotAllowed
.. autoexception:: time2relax.PreconditionFailed
.. autoexception:: time2relax.ResourceConflict
.. autoexception:: time2relax.ResourceNotFound
.. autoexception:: time2relax.ServerError
.. autoexception:: time2relax.Unauthorized

Encodings
---------

.. autofunction:: time2relax.utils.encode_attachment_id
.. autofunction:: time2relax.utils.encode_document_id
.. autofunction:: time2relax.utils.encode_uri_component
.. autofunction:: time2relax.utils.query_method_kwargs

Utilities
---------

.. autofunction:: time2relax.utils.get_database_host
.. autofunction:: time2relax.utils.get_database_name
.. autofunction:: time2relax.utils.raise_http_exception
