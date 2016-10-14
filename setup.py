#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.


import re
import os.path as op


from codecs import open
from setuptools import setup, find_packages


def read(fname):
    ''' Return the file content. '''
    here = op.abspath(op.dirname(__file__))
    with open(op.join(here, fname), 'r', 'utf-8') as fd:
        return fd.read()

readme = read('README.rst')
changelog = read('docs/CHANGELOG.rst').replace('.. _changelog:', '')

install_requirements = [
    'requests',
    'xmltodict',
    'lxml',
]

version = ''
version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    read(op.join('fnapy', '__init__.py')),
                    re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(
    name='fnapy',
    author='Taurus Olson',
    author_email='taurusolson@gmail.com',
    version=version,
    description='A Python API for FNAC WebServices',
    long_description=readme + '\n\n' + changelog,
    keywords=['api', 'fnac', 'python', 'webservices'],
    packages=find_packages(),
    install_requires=install_requirements,
    zip_safe=True,
    license='MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
