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
from tests import response_is_valid, response_is_not_valid


def test_update_offers():
    assert response_is_valid('update_offers', 'offers_update')


def test_update_offers_without_offer_reference():
    assert response_is_not_valid('update_offers_without_offer_reference', 'offers_update')


def test_query_offers():
    assert response_is_valid('query_offers', 'offers_query')


def test_query_offers_with_multiple_parameters():
    assert response_is_valid('query_offers_with_multiple_parameters', 'offers_query')


def test_delete_offers():
    assert response_is_valid('delete_offers', 'offers_update')
