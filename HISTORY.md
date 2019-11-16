# Version History

## 0.6.0 (unreleased)

- Drop Python 2.7 support - Python 2.7 will not be maintained past 2020.

## 0.5.0 (2018-08-04)

- Move the time2relax API to `time2relax.time2relax`.
- Add Python 3.7 support.

## 0.4.1 (2017-11-22)

- Fix Travis build errors - invalid config

## 0.4.0 (2017-11-21)

- `CouchDBError` is now `HTTPError` (*Backwards Incompatible*)
- `CouchDB(skip_setup=False)` is now `CouchDB(create_db=True)` (*Backwards Incompatible*)
- Add Python 3.6 support.
- Drop Python 2.6 support - Python 2.6 is no longer supported by the Python core team. (*Backwards Incompatible*)

## 0.3.0 (2017-03-03)

- New time2relax API. (*Backwards Incompatible*)
- time2relax is now a thin `requests` wrapper.
- New design document functions; `list`, `show`, `view`.

## 0.2.0 (2016-12-10)

- Add Python 3.3, 3.4, 3.5 support.

## 0.1.0 (2016-12-10)

- First release on PyPI.
