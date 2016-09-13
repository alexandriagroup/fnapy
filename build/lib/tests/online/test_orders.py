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
from tests import response_is_valid


def test_update_orders():
    assert response_is_valid('update_orders', 'orders_update')


def test_query_orders():
    assert response_is_valid('query_orders', 'orders_query')


def test_query_orders_created_between_dates():
    assert response_is_valid('query_orders_created_between_dates', 'orders_query')

