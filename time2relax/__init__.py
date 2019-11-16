#             __
# _|_ o __  _  _) __ _  |  _
#  |_ | |||(/_/__ | (/_ | (_|><
#

"""A CouchDB driver for Python.

Example::

    >>> from time2relax import CouchDB
    >>> db = CouchDB('http://localhost:5984/dbname')
    >>> db.insert({'title': 'Ziggy Stardust'})
    <Response [201]>
"""

from __future__ import absolute_import

from time2relax.__version__ import (  # noqa: F401 isort:skip
    __author__, __author_email__, __copyright__, __couch__, __description__, __license__, __title__, __url__,
    __version__)
from time2relax.exceptions import (  # noqa: F401 isort:skip
    BadRequest, Forbidden, HTTPError, MethodNotAllowed, PreconditionFailed, ResourceConflict, ResourceNotFound,
    ServerError, Unauthorized)
from time2relax.models import CouchDB  # noqa: F401 isort:skip
