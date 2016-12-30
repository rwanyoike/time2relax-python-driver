# -*- coding: utf-8 -*-

import pytest
from time2relax import CouchDB, BadRequest, Unauthorized, Forbidden, \
    ResourceNotFound, MethodNotAllowed, ResourceConflict, PreconditionFailed, \
    ServerError, CouchDBError


def test_check_response():
    class Response:
        def __init__(self, status_code):
            self.status_code = status_code

        def json(self):
            return {'reason': None}

    exceptions = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: ResourceNotFound,
        405: MethodNotAllowed,
        409: ResourceConflict,
        412: PreconditionFailed,
        500: ServerError,
        999: CouchDBError,
    }

    for i in exceptions:
        with pytest.raises(exceptions[i]):
            CouchDB._check_response(Response(i))
