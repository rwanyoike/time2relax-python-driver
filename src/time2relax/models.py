"""Primary objects that power time2relax."""

from posixpath import join as urljoin

from requests import Request, Session

from time2relax import exceptions, time2relax, utils


class CouchDB:
    """Representation of a CouchDB database.

    Provides URL-parameter encoding, modeled Exceptions, and database initialization.

    Example::

        >>> import time2relax
        >>> db = time2relax.CouchDB('http://localhost:5984/testdb')
        >>> db.insert({'title': 'Ziggy Stardust'})
        <Response [201]>
    """

    _created = False

    def __init__(self, url, create_db=True):
        """Initialize the database object.

        :param str url: The Database URL.
        :param bool create_db: (optional) Create the database.
        """
        # Raise exception on an invalid URL
        Request("HEAD", url).prepare()

        #: Database host
        self.host = utils.get_database_host(url)

        #: Database name
        self.name = utils.get_database_name(url)

        #: Database URL
        # FIXME: Converts "test.db/a/b/index.html?e=f" to "test.db/index.html"
        self.url = urljoin(self.host, self.name)

        #: Database initialization
        self.create_db = create_db

        #: Default :class:`requests.Session`
        self.session = Session()
        # http://docs.couchdb.org/en/stable/api/basics.html#request-headers
        self.session.headers["Accept"] = "application/json"

    def __repr__(self):
        """Return repr(self)."""
        return f"<{self.__class__.__name__} [{self.url}]>"

    @utils.relax(time2relax.all_docs)
    def all_docs(self, **kwargs):
        """Fetch multiple documents."""

    @utils.relax(time2relax.bulk_docs)
    def bulk_docs(self, docs, **kwargs):
        """Create, update or delete multiple documents."""

    @utils.relax(time2relax.compact)
    def compact(self, **kwargs):
        """Trigger a compaction operation."""

    @utils.relax(time2relax.ddoc_list)
    def ddoc_list(self, ddoc_id, func_id, view_id, other_id=None, **kwargs):
        """Apply a list function against a view."""

    @utils.relax(time2relax.ddoc_show)
    def ddoc_show(self, ddoc_id, func_id, doc_id=None, **kwargs):
        """Apply a show function against a document."""

    @utils.relax(time2relax.ddoc_view)
    def ddoc_view(self, ddoc_id, func_id, **kwargs):
        """Execute a view function."""

    @utils.relax(time2relax.destroy)
    def destroy(self, **kwargs):
        """Delete the database."""
        m, p, k = time2relax.destroy(**kwargs)
        return self.request(m, p, _init=False, **k)

    @utils.relax(time2relax.get)
    def get(self, doc_id, **kwargs):
        """Retrieve a document."""

    @utils.relax(time2relax.get_att)
    def get_att(self, doc_id, att_id, **kwargs):
        """Retrieve an attachment."""

    @utils.relax(time2relax.info)
    def info(self, **kwargs):
        """Get information about the database."""

    @utils.relax(time2relax.insert)
    def insert(self, doc, **kwargs):
        """Create or update an existing document."""

    @utils.relax(time2relax.insert_att)
    # pylint: disable=too-many-arguments
    def insert_att(self, doc_id, doc_rev, att_id, att, att_type, **kwargs):
        """Create or update an existing attachment."""

    @utils.relax(time2relax.remove)
    def remove(self, doc_id, doc_rev, **kwargs):
        """Delete a document."""

    @utils.relax(time2relax.remove_att)
    def remove_att(self, doc_id, doc_rev, att_id, **kwargs):
        """Delete an attachment."""

    def replicate_to(self, target, **kwargs):
        """Replicate data from a source (this) to target."""
        m, p, k = time2relax.replicate_to(self.url, target, **kwargs)
        return self.request(m, p, _init=False, **k)

    def request(self, method, path, _init=True, **kwargs):
        """Construct a :class:`requests.Request` object and send it."""
        # Check if the database exists
        if _init and self.create_db and (not self._created):
            try:
                self.request("HEAD", "", _init=False)
            except exceptions.ResourceNotFound:
                self.request("PUT", "", _init=False)
            self._created = True

        return time2relax.request(self.session, self.url, method, path, **kwargs)
