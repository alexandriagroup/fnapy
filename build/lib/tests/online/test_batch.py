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


def test_get_batch_status():
    assert response_is_valid('get_batch_status', 'batch_status')


def test_query_batch():
    assert response_is_valid('query_batch', 'batch_query')




