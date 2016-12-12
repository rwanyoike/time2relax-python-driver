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
    'requests==2.12.3',
]

test_requirements = [
    'pytest==3.0.5',
    'PyYAML==3.12',
    'responses==0.5.1',
]

setup(
    name='time2relax',
    version='0.2.0',
    description='CouchDB driver for Python.',
    long_description=readme + '\n\n' + history,
    author='Raymond Wanyoike',
    author_email='raymond.wanyoike@gmail.com',
    url='https://github.com/rwanyoike/time2relax',
    packages=[
        'time2relax',
    ],
    package_dir={
        'time2relax': 'time2relax'
    },
    include_package_data=True,
    setup_requires=setup_requires,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='couchdb, time2relax',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
