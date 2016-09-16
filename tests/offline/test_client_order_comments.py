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


def test_query_client_order_comments(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_client_order_comments',
                                          'client_order_comments_query')
    with context:
        fake_manager.query_client_order_comments(paging=1)


def test_update_client_order_comments(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'update_client_order_comments',
                                          'client_order_comments_update')
    with context:
        fake_manager.update_client_order_comments(seller_comment='Hello',
                                                  order_fnac_id='8D7472DB-7EAF-CE05-A960-FC12B812FA14')




