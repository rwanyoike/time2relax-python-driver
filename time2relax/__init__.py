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

    >>> import time2relax
    >>> db = time2relax.CouchDB('http://localhost:5984/testdb')
    >>> r = db.insert({'title': 'Ziggy Stardust'})
    >>> r.status_code
    201
    >>> r.json()['ok']
    True

:copyright: \(c\) Raymond Wanyoike.
:license: MIT, see LICENSE for more details.
"""

from .__version__ import (  # noqa: F401
    __title__, __description__, __url__, __version__, __author__,
    __author_email__, __license__, __copyright__, __relax__)

from . import utils  # noqa: F401
from .models import CouchDB  # noqa: F401
from .exceptions import (  # noqa: F401
    BadRequest, Unauthorized, Forbidden, ResourceNotFound, MethodNotAllowed,
    ResourceConflict, PreconditionFailed, ServerError, CouchDBError)
