"""Primary methods that power time2relax."""

import json
from posixpath import join as urljoin

from requests import compat

from time2relax import utils  # pylint: disable=import-self

_LIST = "_list"
_SHOW = "_show"
_VIEW = "_view"


def all_docs(**kwargs):
    """Fetch multiple documents.

    - http://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_all_docs
    - http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs

    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if "params" in kwargs:
        params = kwargs["params"]
        del kwargs["params"]
    else:
        params = None

    method, _kwargs = utils.query_method_kwargs(params)
    kwargs.update(_kwargs)

    return method, "_all_docs", kwargs


def bulk_docs(docs, **kwargs):
    """Create, update or delete multiple documents.

    http://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_bulk_docs

    :param list docs: The sequence of documents to be sent.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if ("json" not in kwargs) or (not isinstance(kwargs["json"], dict)):
        kwargs["json"] = {}

    kwargs["json"]["docs"] = docs

    return "POST", "_bulk_docs", kwargs


def compact(**kwargs):
    """Trigger a compaction operation.

    http://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact

    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if "headers" not in kwargs or (not isinstance(kwargs["headers"], dict)):
        kwargs["headers"] = {}

    kwargs["headers"]["Content-Type"] = "application/json"

    return "POST", "_compact", kwargs


def ddoc_list(ddoc_id, func_id, view_id, other_id=None, **kwargs):
    """Apply a list function against a view.

    http://docs.couchdb.org/en/stable/api/ddoc/render.html#get--db-_design-ddoc-_list-func-view

    :param str ddoc_id: The design document name.
    :param str func_id: The list function name.
    :param str view_id: The view function name.
    :param str other_id: (optional) Other design document that holds the view function.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if other_id:
        path = urljoin(utils.encode_document_id(other_id), view_id)
    else:
        path = view_id

    return _ddoc("GET", ddoc_id, _LIST, func_id, path, **kwargs)


def ddoc_show(ddoc_id, func_id, doc_id=None, **kwargs):
    """Apply a show function against a document.

    http://docs.couchdb.org/en/stable/api/ddoc/render.html#get--db-_design-ddoc-_show-func

    :param str ddoc_id: The design document name.
    :param str func_id: The show function name.
    :param str doc_id: (optional) The document to execute the show function on.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if doc_id:
        return _ddoc(
            "GET", ddoc_id, _SHOW, func_id, utils.encode_document_id(doc_id), **kwargs
        )

    return _ddoc("GET", ddoc_id, _SHOW, func_id, **kwargs)


def ddoc_view(ddoc_id, func_id, **kwargs):
    """Execute a view function.

    http://docs.couchdb.org/en/stable/api/ddoc/views.html#get--db-_design-ddoc-_view-view

    :param str ddoc_id: The design document name.
    :param str func_id: The view function name.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if "params" in kwargs:
        params = kwargs["params"]
        del kwargs["params"]
    else:
        params = None

    method, _kwargs = utils.query_method_kwargs(params)
    kwargs.update(_kwargs)

    return _ddoc(method, ddoc_id, _VIEW, func_id, **kwargs)


def destroy(**kwargs):
    """Delete the database.

    http://docs.couchdb.org/en/stable/api/database/common.html#delete--db

    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    return "DELETE", "", kwargs


def get(doc_id, **kwargs):
    """Retrieve a document.

    http://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid

    :param str doc_id: The document to retrieve.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if (
        ("params" in kwargs)
        and (isinstance(kwargs["params"], dict))
        and ("open_revs" in kwargs["params"])
        and (kwargs["params"]["open_revs"] != "all")
    ):
        # 'open_revs' needs to be JSON encoded
        kwargs["params"]["open_revs"] = json.dumps(kwargs["params"]["open_revs"])

    path = utils.encode_document_id(doc_id)

    return "GET", path, kwargs


def get_att(doc_id, att_id, **kwargs):
    """Retrieve an attachment.

    http://docs.couchdb.org/en/stable/api/document/attachments.html#get--db-docid-attname

    :param str doc_id: The attachment document.
    :param str att_id: The attachment to retrieve.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    path = urljoin(utils.encode_document_id(doc_id), utils.encode_attachment_id(att_id))

    return "GET", path, kwargs


def info(**kwargs):
    """Get information about the database.

    http://docs.couchdb.org/en/stable/api/database/common.html#get--db

    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    return "GET", "", kwargs


def insert(doc, **kwargs):
    """Create or update an existing document.

    - http://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
    - http://docs.couchdb.org/en/stable/api/database/common.html#post--db

    :param dict doc: The document to insert.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    kwargs["json"] = doc

    if "_id" in doc:
        return "PUT", utils.encode_document_id(doc["_id"]), kwargs

    return "POST", "", kwargs


def insert_att(doc_id, doc_rev, att_id, att, att_type, **kwargs):
    """Create or update an existing attachment.

    http://docs.couchdb.org/en/stable/api/document/attachments.html#put--db-docid-attname

    :param str doc_id: The attachment document.
    :param doc_rev: (optional) The document revision.
    :param str att_id: The attachment name.
    :param att: The dictionary, bytes, or file-like object to insert.
    :param str att_type: The attachment MIME type.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if doc_rev:
        if ("params" not in kwargs) or (not isinstance(kwargs["params"], dict)):
            kwargs["params"] = {}
        kwargs["params"]["rev"] = doc_rev

    if ("headers" not in kwargs) or (not isinstance(kwargs["headers"], dict)):
        kwargs["headers"] = {}

    path = urljoin(utils.encode_document_id(doc_id), utils.encode_attachment_id(att_id))
    kwargs["headers"]["Content-Type"] = att_type
    kwargs["data"] = att

    return "PUT", path, kwargs


def remove(doc_id, doc_rev, **kwargs):
    """Delete a document.

    http://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid

    :param str doc_id: The document to remove.
    :param str doc_rev: The document revision.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if ("params" not in kwargs) or (not isinstance(kwargs["params"], dict)):
        kwargs["params"] = {}

    path = utils.encode_document_id(doc_id)
    kwargs["params"]["rev"] = doc_rev

    return "DELETE", path, kwargs


def remove_att(doc_id, doc_rev, att_id, **kwargs):
    """Delete an attachment.

    http://docs.couchdb.org/en/stable/api/document/attachments.html#delete--db-docid-attname

    :param str doc_id: The attachment document.
    :param str doc_rev: The document revision.
    :param str att_id: The attachment to remove.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    if ("params" not in kwargs) or (not isinstance(kwargs["params"], dict)):
        kwargs["params"] = {}

    path = urljoin(utils.encode_document_id(doc_id), utils.encode_attachment_id(att_id))
    kwargs["params"]["rev"] = doc_rev

    return "DELETE", path, kwargs


def replicate_to(source, target, **kwargs):
    """Replicate data from source (this) to target.

    http://docs.couchdb.org/en/stable/api/server/common.html#replicate

    :param str target: The URL or name of the target database.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    url = urljoin(utils.get_database_host(source), "_replicate")

    if ("json" not in kwargs) or (not isinstance(kwargs["json"], dict)):
        kwargs["json"] = {}

    kwargs["json"]["source"] = source
    kwargs["json"]["target"] = target

    return "POST", url, kwargs


def request(session, base_path, method, path, **kwargs):
    """Construct a :class:`requests.Request` object and send it.

    :param requests.Session session:
    :param str base_path:
    :param str method: Method for the :class:`requests.Request` object.
    :param str path: (optional) The path to join with :attr:`CouchDB.url`.
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: requests.Response
    """
    # Prepare the params dictionary
    if ("params" in kwargs) and isinstance(kwargs["params"], dict):
        params = kwargs["params"].copy()
        for key, val in params.items():
            # Handle titlecase booleans
            if isinstance(val, bool):
                params[key] = json.dumps(val)
        kwargs["params"] = params

    if compat.urlparse(path).scheme:
        # Support absolute URLs
        url = path
    else:
        url = urljoin(base_path, path).strip("/")

    r = session.request(method, url, **kwargs)
    # Raise exception on a bad status code
    if not (200 <= r.status_code < 300):
        utils.raise_http_exception(r)

    return r


def _ddoc(method, ddoc_id, func_type, func_id, _path=None, **kwargs):
    """Apply or execute a design document function.

    :param str method: Method for the :class:`requests.Request` object.
    :param str ddoc_id: The design document name.
    :param str func_type: The design function type.
    :param str func_id: The design function name.
    :param str _path: (internal)
    :param kwargs: (optional) Arguments that :meth:`requests.Session.request` takes.
    :rtype: (str, str, dict)
    """
    doc_id = urljoin("_design", ddoc_id)
    path = urljoin(utils.encode_document_id(doc_id), func_type, func_id)

    if _path:
        path = urljoin(path, _path)

    return method, path, kwargs
