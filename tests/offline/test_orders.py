# Python modules
from __future__ import unicode_literals
import os
from datetime import datetime

# Third-party modules
import pytest
import pytz

# Project modules
from fnapy.fnapy_manager import FnapyManager
from fnapy.config import ORDER_ELEMENTS
from tests import make_requests_get_mock, fake_manager, offers_data


def test_query_orders(monkeypatch, fake_manager):
    """query_orders should return the orders placed by customers"""
    monkeypatch.setattr('requests.post', make_requests_get_mock('query_orders.xml'))
    orders_query_response = fake_manager.query_orders()
    orders_query_dict = orders_query_response.dict['orders_query_response']
    orders = orders_query_dict['order']

    # We should have a list of orders
    assert isinstance(orders, (list, tuple))

    # There should be 3 orders
    assert len(orders) == 3

    # The elements in the order element should contain valid sub-elements
    assert all(x in ORDER_ELEMENTS for x in orders[0].keys())


def test_update_orders(monkeypatch, fake_manager):
    pass
