#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('docs/readme.rst') as readme_file:
    readme = readme_file.read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'six',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'responses',
]

setup(
    name='time2relax',
    version='0.3.0',
    description='A CouchDB driver for Python.',
    long_description=readme + '\n\n' + history,
    author='Raymond Wanyoike',
    author_email='raymond.wanyoike@gmail.com',
    url='https://github.com/rwanyoike/time2relax',
    packages=find_packages(include=['time2relax']),
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
