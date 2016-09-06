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


def test_update_offers():
    response_is_valid('update_offers', 'offers_update')


def test_query_offers():
    response_is_valid('query_offers', 'offers_query')


def test_get_batch_status():
    response_is_valid('get_batch_status', 'batch_status')


