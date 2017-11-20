# -*- coding: utf-8 -*-

#             __
# _|_ o __  _  _) __ _  |  _
#  |_ | |||(/_/__ | (/_ | (_|><
#

"""
time2relax: Python CouchDB Driver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

time2relax is a Python CouchDB driver that tries to offer a minimal level of
abstraction between you and CouchDB. Basic insert usage::

    >>> from time2relax import CouchDB
    >>> db = CouchDB('http://localhost:5984/dbname')
    >>> db.insert({'title': 'Ziggy Stardust'})
    <Response [201]>
"""

from .__version__ import (  # noqa: F401
    __title__, __description__, __url__, __version__, __author__, __author_email__, __license__,
    __copyright__, __relax__)

from . import utils  # noqa: F401

from .models import CouchDB  # noqa: F401
from .exceptions import (  # noqa: F401
    BadRequest, Unauthorized, Forbidden, ResourceNotFound, MethodNotAllowed, ResourceConflict,
    PreconditionFailed, ServerError, HTTPError)
