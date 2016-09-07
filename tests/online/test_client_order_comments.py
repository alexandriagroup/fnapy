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


def test_update_client_order_comments():
    assert response_is_valid('update_client_order_comments', 'client_order_comments_update')


def test_query_client_order_comments():
    assert response_is_valid('query_client_order_comments', 'client_order_comments_query')

