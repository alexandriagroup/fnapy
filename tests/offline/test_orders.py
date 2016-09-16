# Python modules
from __future__ import unicode_literals

# Third-party modules
import pytest

# Project modules
from tests import fake_manager
from tests.offline import create_context_for_requests


def test_query_orders(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_orders', 'orders_query')
    with context:
        fake_manager.query_orders(results_count=10, paging=1)


def test_update_orders(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'update_orders', 'orders_update')
    with context:
        action1 = {"order_detail_id": 1, "action": "Accepted"}
        action2 = {"order_detail_id": 2, "action": "Refused"}
        fake_manager.update_orders(order_id="57BEAFDA828A8",
                                   order_update_action='accept_order',
                                   actions=[action1, action2])
