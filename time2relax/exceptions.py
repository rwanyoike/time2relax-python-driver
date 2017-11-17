# -*- coding: utf-8 -*-

"""
time2relax.exceptions
~~~~~~~~~~~~~~~~~~~~~

This module contains the set of time2relax exceptions.
"""


class CouchDBError(Exception):
    """A HTTP error occurred."""


class BadRequest(CouchDBError):
    """A 400 HTTP error."""


class Unauthorized(CouchDBError):
    """A 401 HTTP error."""


class Forbidden(CouchDBError):
    """A 403 HTTP error."""


class ResourceNotFound(CouchDBError):
    """A 404 HTTP error."""


class MethodNotAllowed(CouchDBError):
    """A 405 HTTP error."""


class ResourceConflict(CouchDBError):
    """A 409 HTTP error."""


class PreconditionFailed(CouchDBError):
    """A 412 HTTP error."""


class ServerError(CouchDBError):
    """A 500 HTTP error."""
