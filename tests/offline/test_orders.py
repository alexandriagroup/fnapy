# Python modules
from __future__ import unicode_literals

# Third-party modules
import pytest

# Project modules
from tests import fake_manager
from tests.offline import ContextualTest


def test_query_orders(monkeypatch, fake_manager):
    context = ContextualTest(monkeypatch, fake_manager, 'query_orders', 'orders_query')
    with context:
        fake_manager.query_orders(results_count=10, paging=1)


def test_update_orders(monkeypatch, fake_manager):
    context = ContextualTest(monkeypatch, fake_manager, 'update_orders', 'orders_update')
    with context:
        action1 = {"order_detail_id": 1, "action": "Accepted"}
        action2 = {"order_detail_id": 2, "action": "Refused"}
        fake_manager.update_orders(order_id="57BEAFDA828A8",
                                   order_update_action='accept_order',
                                   actions=[action1, action2])


# def test_query_orders(monkeypatch, fake_manager):
#     """query_orders should return the orders placed by customers"""
#     monkeypatch.setattr('requests.post', make_requests_get_mock('query_orders.xml'))
#     orders_query_response = fake_manager.query_orders()
#     orders_query_dict = orders_query_response.dict['orders_query_response']
#     orders = orders_query_dict['order']

#     # We should have a list of orders
#     assert isinstance(orders, (list, tuple))

#     # There should be 3 orders
#     assert len(orders) == 3

#     # The elements in the order element should contain valid sub-elements
#     assert all(x in ORDER_ELEMENTS for x in orders[0].keys())


