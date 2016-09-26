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

        r = self.session.request(method, url, **kwargs)

        if not (200 <= r.status_code < 400):
            self._handle_error(r)

        # Return requests.Response
        return r

    def _handle_error(self, response):
        """Handles any non [2|3]xx status."""

        try:
            message = response.json()
        except ValueError:
            message = None

        args = (message, response)

        if response.status_code == 400:
            raise BadRequest(*args)
        if response.status_code == 401:
            raise Unauthorized(*args)
        if response.status_code == 403:
            raise Forbidden(*args)
        if response.status_code == 404:
            raise ResourceNotFound(*args)
        if response.status_code == 405:
            raise MethodNotAllowed(*args)
        if response.status_code == 409:
            raise ResourceConflict(*args)
        if response.status_code == 412:
            raise PreconditionFailed(*args)
        if response.status_code == 500:
            raise ServerError(*args)

        raise CouchDbError(*args)
