# -*- coding: utf-8 -*-

"""
time2relax.exceptions
~~~~~~~~~~~~~~~~~~~~~

This module contains the set of time2relax exceptions.
"""


class HTTPError(Exception):
    """A HTTP error occurred."""


class BadRequest(HTTPError):
    """A 400 HTTP error."""


class Unauthorized(HTTPError):
    """A 401 HTTP error."""


class Forbidden(HTTPError):
    """A 403 HTTP error."""


class ResourceNotFound(HTTPError):
    """A 404 HTTP error."""


class MethodNotAllowed(HTTPError):
    """A 405 HTTP error."""


class ResourceConflict(HTTPError):
    """A 409 HTTP error."""


class PreconditionFailed(HTTPError):
    """A 412 HTTP error."""


class ServerError(HTTPError):
    """A 500 HTTP error."""
