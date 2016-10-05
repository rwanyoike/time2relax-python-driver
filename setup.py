#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requires = [
    'pytest-runner==2.9',
]

requirements = [
    'requests==2.11.1',
]

test_requirements = [
    'pytest==3.0.3',
    'PyYAML==3.12',
    'responses==0.5.1',
]

setup(
    name='time2relax',
    version='0.1.0',
    description="CouchDB driver for Python.",
    long_description=readme + '\n\n' + history,
    author="Raymond Wanyoike",
    author_email='raymond.wanyoike@gmail.com',
    url='https://github.com/rwanyoike/time2relax',
    packages=[
        'time2relax',
    ],
    package_dir={'time2relax': 'time2relax'},
    include_package_data=True,
    setup_requires=setup_requires,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='couchdb, time2relax',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
