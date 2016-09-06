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


def test_update_orders():
    create_test('update_orders', 'orders_update')


def test_query_orders():
    create_test('query_orders', 'orders_query')

