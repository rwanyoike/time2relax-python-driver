# -*- coding: utf-8 -*-

from requests import Session

from .errors import BadRequest, ResourceConflict, CouchDbError, \
    MethodNotAllowed, ServerError, ResourceNotFound, Unauthorized, Forbidden, \
    PreconditionFailed


class HTTPClient(object):
    """Base HTTP client. (Requests HTTP library)"""

    def __init__(self):
        """Initialize a HTTP client object."""

        # Session with cookie persistence
        self.session = Session()

    def request(self, method, url, **kwargs):
        """Constructs and sends a request."""

        r = self.session.request(method, url, **kwargs)
        self._handle(r)

        return r.json(), r.status_code, r.headers

    def _handle(self, r):
        """Handles any >= 400 status code."""

        if r.status_code <= 399:
            return

        if len(r.content) > 3:
            err = r.json()
        else:
            err = None

        args = (err, r.status_code)

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
