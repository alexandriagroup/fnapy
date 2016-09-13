#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.


from setuptools import setup, find_packages

requirements = [
    'requests',
    'xmltodict',
    'lxml',
    'bs4'
]

setup_requirements = [
    'pbr>=1.9', 'setuptools>=17.1'
]

setup(
    name='fnapy',
    author='Taurus Olson',
    author_email='taurusolson@gmail.com',
    version='0.1',
    description='A Python API for FNAC WebServices',
    keywords=['api', 'fnac', 'python', 'webservices'],
    packages=find_packages(),
    install_requires=requirements,
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
