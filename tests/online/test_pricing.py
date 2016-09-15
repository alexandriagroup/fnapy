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


def test_query_pricing():
    assert response_is_valid('query_pricing', 'pricing_query')


def test_query_pricing_with_invalid_ean():
    assert response_is_valid('query_pricing_with_invalid_ean', 'pricing_query')


