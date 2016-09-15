#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

# Third-party modules
import pytest

# Projects modules
from fnapy.fnapy_manager import FnapyManager


def test_manager_raises_TypeError_with_invalid_connection():
    """FnapyManager should raise a TypeError when the connection is not a FnapyConnection"""
    with pytest.raises(TypeError):
        connection = {'partner_id': 'XXX', 'shop_id': 'XXX', 'key': 'XXX'}
        manager = FnapyManager(connection)





