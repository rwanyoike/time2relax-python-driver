#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

about = {}
with open('time2relax/__version__.py') as fp:
    exec(fp.read(), about)
with open('docs/readme.rst') as fp:
    readme = fp.read()
with open('docs/history.rst') as fp:
    history = fp.read()

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
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['time2relax'],
    include_package_data=True,
    install_requires=requirements,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
)
