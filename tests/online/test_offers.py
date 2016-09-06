#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Online tests for fnapy
"""

# Project modules
from fnapy.config import *
from tests import create_test


def test_update_offers():
    create_test('update_offers', 'offers_update')


def test_query_offers():
    create_test('query_offers', 'offers_query')

