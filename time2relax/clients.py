# -*- coding: utf-8 -*-

from requests import Session

from .errors import (BadRequest, ResourceConflict, CouchDbError,
                     MethodNotAllowed, ServerError, ResourceNotFound,
                     Unauthorized, Forbidden, PreconditionFailed)


class HTTPClient(object):
    """Base HTTP client. (Requests HTTP library)"""

    def __init__(self):
        """Initialize a HTTP client object."""

        # Session with cookie persistence
        self.session = Session()

    def request(self, method, url, **kwargs):
        """Constructs and sends a request."""

        # Pipe to HTTP library
        r = self.session.request(method, url, **kwargs)

        if not (200 <= r.status_code < 400):
            self._handle_error(r)

        # json + headers = simple
        return r.json(), r.headers

    def _handle_error(self, r):
        """Handles any non [2|3]xx status."""

        try:
            message = r.json()
        except ValueError:
            message = None

        args = (message, r.headers, r.status_code)

        if r.status_code == 400:
            raise BadRequest(*args)
        if r.status_code == 401:
            raise Unauthorized(*args)
        if r.status_code == 403:
            raise Forbidden(*args)
        if r.status_code == 404:
            raise ResourceNotFound(*args)
        if r.status_code == 405:
            raise MethodNotAllowed(*args)
        if r.status_code == 409:
            raise ResourceConflict(*args)
        if r.status_code == 412:
            raise PreconditionFailed(*args)
        if r.status_code == 500:
            raise ServerError(*args)

        raise CouchDbError(*args)
