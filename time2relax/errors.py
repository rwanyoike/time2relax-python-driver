# -*- coding: utf-8 -*-


class CouchDbError(Exception):
    """Class for errors based on HTTP status codes >= 400."""

    def __init__(self, message, headers=None, status_code=None):
        """Initialize the error object."""

        super(CouchDbError, self).__init__(message)
        self.headers = headers
        self.status_code = status_code


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class BadRequest(CouchDbError):
    """Exception raised when a 400 HTTP error is received."""

    pass


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class Unauthorized(CouchDbError):
    """Exception raised when a 401 HTTP error is received."""

    pass


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class Forbidden(CouchDbError):
    """Exception raised when a 403 HTTP error is received."""

    pass


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class ResourceNotFound(CouchDbError):
    """Exception raised when a 404 HTTP error is received."""

    pass


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class MethodNotAllowed(CouchDbError):
    """Exception raised when a 405 HTTP error is received."""

    pass


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class ResourceConflict(CouchDbError):
    """Exception raised when a 409 HTTP error is received."""

    pass


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class PreconditionFailed(CouchDbError):
    """Exception raised when a 412 HTTP error is received."""

    pass


# http://docs.couchdb.org/en/latest/api/basics.html?#http-status-codes
class ServerError(CouchDbError):
    """Exception raised when a 500 HTTP error is received."""

    pass
