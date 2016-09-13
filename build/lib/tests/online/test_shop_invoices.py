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


def test_query_shop_invoices():
    assert response_is_valid('query_shop_invoices', 'shop_invoices_query')

