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
from fnapy.utils import *
from fnapy.config import *
from tests import response_is_valid


# def test_update_incidents():
#     create_test('update_incidents', 'incidents_update')


def test_query_incidents():
    assert response_is_valid('query_incidents', 'incidents_query')
