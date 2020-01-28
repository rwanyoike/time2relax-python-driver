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

from time2relax.exceptions import (  # noqa: F401
    BadRequest,
    Forbidden,
    HTTPError,
    MethodNotAllowed,
    PreconditionFailed,
    ResourceConflict,
    ResourceNotFound,
    ServerError,
    Unauthorized,
)
from time2relax.models import CouchDB  # noqa: F401
