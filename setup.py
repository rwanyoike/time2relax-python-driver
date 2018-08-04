#!/usr/bin/env python

# io.open is needed for projects that support Python 2.7. It ensures open()
# defaults to text mode  with universal newlines, and accepts an argument to
# specify the text encoding. Python 3 only projects can skip this import.
from io import open

from setuptools import setup

with open('time2relax/__version__.py') as fp:
    about = {}
    exec(fp.read(), about)

with open('README.md') as fp:
    readme = fp.read()

with open('HISTORY.md') as fp:
    history = fp.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description='\n---\n'.join([readme, history]),
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['time2relax'],
    include_package_data=True,
    install_requires=['requests>=2,<3', 'six'],
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=['pytest', 'pytest-mock'],
)
