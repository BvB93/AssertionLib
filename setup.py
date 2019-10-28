#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit assertionlib/__version__.py
version = {}
with open(os.path.join(here, 'assertionlib', '__version__.py')) as f:
    exec(f.read(), version)

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='AssertionLib',
    version=version['__version__'],
    description=('A package for performing assertions and providing informative exception messages.'),
    long_description=readme + '\n\n',
    long_description_content_type='text/x-rst',
    author=['B. F. van Beek'],
    author_email='b.f.van.beek@vu.nl',
    url='https://github.com/nlesc-nano/AssertionLib',
    packages=['assertionlib'],
    package_dir={'assertionlib': 'assertionlib'},
    package_data={'assertionlib': ['*.rst']},
    include_package_data=True,
    license='GNU Lesser General Public License v3 or later',
    zip_safe=False,
    keywords=[
        'assertion',
        'assertions',
        'assertion-library',
        'python-3',
        'python-3-6',
        'python-3-7',
        'python-3-8'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    test_suite='tests',
    python_requires='>=3.6',
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle'
    ],
    extras_require={
        'test': ['pytest', 'pytest-cov', 'pycodestyle'],
        'doc': ['sphinx>=2.0', 'sphinx_rtd_theme', 'sphinx-autodoc-typehints']
    }
)
