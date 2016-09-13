#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.


import os
from setuptools import setup, find_packages

install_requirements = [
    'requests',
    'xmltodict',
    'lxml',
    'bs4'
]

setup_requirements = [
    'pbr>=1.9', 'setuptools>=17.1'
]

def is_not_in_travis():
    return not os.getcwd().startswith('/home/travis')


setup(
    name='fnapy',
    author='Taurus Olson',
    author_email='taurusolson@gmail.com',
    description='A Python API for FNAC WebServices',
    keywords=['api', 'fnac', 'python', 'webservices'],
    packages=find_packages(),
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    pbr=is_not_in_travis(),
    zip_safe=True,
    license='MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
