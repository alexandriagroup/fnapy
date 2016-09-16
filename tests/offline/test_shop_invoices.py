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
from tests.offline import create_context_for_requests


def test_query_shop_invoices(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_shop_invoices',
                                          'shop_invoices_query')
    with context:
        fake_manager.query_shop_invoices(paging=1, results_count=100)


