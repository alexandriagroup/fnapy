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


def test_query_incidents(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_incidents', 'incidents_query')
    with context:
        fake_manager.query_incidents(paging=1, results_count=100)


def test_update_incidents(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'update_incidents',
                                          'incidents_update')
    with context:
        reasons =  [{"order_detail_id": 2, "refund_reason": 'no_stock'}]
        fake_manager.update_incidents(order_id='57BEAFDA828A8',
                                      incident_update_action='refund',
                                      reasons=reasons)


