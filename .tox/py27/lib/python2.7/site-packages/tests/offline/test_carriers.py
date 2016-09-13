#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

# Python modules
from __future__ import unicode_literals

# Project modules
from tests import make_requests_get_mock, fake_manager
from tests.offline import ContextualTest


def test_query_carriers(monkeypatch, fake_manager):
    context = ContextualTest(monkeypatch, fake_manager, 'query_carriers', 'carriers_query')
    with context:
        fake_manager.query_carriers()


