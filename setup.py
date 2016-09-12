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
    version='0.1',
    install_requires=requirements,
    setup_requires=setup_requirements,
    pbr=True,
    zip_safe=True,
)
