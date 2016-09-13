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

# Python modules
from __future__ import unicode_literals
import os
from datetime import datetime
from collections import OrderedDict

# Third-party modules
import pytest
import pytz

# Project modules
from fnapy.fnapy_manager import FnapyManager
from fnapy.utils import Response
from fnapy.config import ORDER_ELEMENTS
from tests import offers_data, setup, save_xml_response


@pytest.mark.skip(reason='No waste of time')
def test_authenticate_returns_token(setup):
    """authenticate should return a token as a unicode"""
    token = setup['manager'].authenticate()
    assert isinstance(token, unicode)
    assert len(token) != 0


@pytest.mark.skip(reason='No waste of time')
def test_update_offers(setup):
    """update_offers should return a response containing batch_id"""
    offers_update_dict = setup['response'].dict['offers_update_response']
    batch_id = offers_update_dict.get('batch_id')
    assert batch_id


@pytest.mark.skip(reason='No waste of time')
def test_update_offers_with_updated_offers(setup):
    """update_offers should really update the offers"""
    # We update the price of offer_data3
    new_price = 40
    offer_data3 = {'product_reference':'9780262510875',
            'offer_reference':'B76A-CD5-444',
            'price':new_price, 'product_state':11, 'quantity':10, 
            'description': 'New product - 2-3 days shipping, from France'}

    manager = setup['manager']
    offers_update_response = manager.update_offers([offer_data3])
    offers_update_dict = offers_update_response.dict['offers_update_response']
    batch_id = offers_update_dict.get('batch_id')

    offers_query_response = manager.query_offers()
    offers_query_dict = offers_query_response.dict['offers_query_response']
    offers = offers_query_dict['offer']

    # The number of offers stay the same
    assert len(offers) == len(offers_data)

    # The updated offer should be updated on the server
    found_offer = False
    for offer in offers:
        if offer.get('offer_seller_id') == 'B76A-CD5-444':
            found_offer = True
            assert int(offer.get('price', -1)) == new_price
    if not found_offer:
        assert False


# TODO Test status when RUNNING then OK
@pytest.mark.skip(reason='No waste of time')
def test_get_batch_status(setup):
    """get_batch_status should return a valid batch_status_response"""
    offers_update_response = setup['response']
    offers_update_dict = offers_update_response.dict['offers_update_response']
    batch_id = offers_update_dict.get('batch_id', '')
    batch_status_response = setup['manager'].get_batch_status(batch_id)
    batch_status_dict = batch_status_response.dict['batch_status_response']
    print batch_status_dict.get('@status')
    assert batch_status_dict.get('@status') == 'ACTIVE'
    save_xml_response(batch_status_response.xml, 'get_batch_status.xml')


@pytest.mark.skip(reason='No waste of time')
def test_query_offers_with_results_count(setup):
    """query_offers should return the first item when paging=1 and results_count=1"""
    offers_query_response = setup['manager'].query_offers(paging=1, results_count=1)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # The offers_query_response has an 'offer' element
    assert offers_query_dict.get('offer')
    assert int(offers_query_dict.get('nb_total_per_page', -1000)) == 1
    save_xml_response(offers_query_response.xml, 'query_offers_with_results_count.xml')


@pytest.mark.skip(reason='No waste of time')
def test_query_offers_with_single_element(setup):
    """query_offers should accept a single parameter"""
    offer_count_expected = 2
    quantity = {'@mode': 'Equals', '@value': 16}
    offers_query_response = setup['manager'].query_offers(quantity=quantity)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # Only 2 offers whose quantity = 16
    offers = offers_query_dict.get('offer', [])
    assert len(offers) == offer_count_expected

    # The offer_seller_id should be the SKU (offer_reference) of the offers
    # with the corresponding criteria
    for i in range(offer_count_expected):
         offers[i].get('offer_seller_id', 'FAILED') == offers_data[i]['offer_reference']
    save_xml_response(offers_query_response.xml, 'query_offers_with_single_element.xml')


@pytest.mark.skip(reason='No waste of time')
def test_query_offers_with_multiple_elements(manager):
    """query_offers should accept queries on multiple elements"""
    offer_count_expected = 2
    dmin = datetime(2016, 8, 23, 0, 0, 0).replace(tzinfo=pytz.utc)
    dmax = datetime(2016, 9, 2, 0, 0, 0).replace(tzinfo=pytz.utc)
    date = {'@type': 'Modified',
    'min': {'#text': dmin.isoformat()},
    'max': {'#text': dmax.isoformat()}
    }
    quantity = {'@mode': 'Equals', '@value': 16}
    offers_query_response = setup['manager'].query_offers(quantity=quantity, date=date)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # Only 2 offers whose quantity = 16 and within the given time range
    offers = offers_query_dict.get('offer', [])
    assert len(offers) == offer_count_expected

    # The offer_seller_id should be the SKU (offer_reference) of the offers
    # with the corresponding criteria
    for i in range(offer_count_expected):
         offers[i].get('offer_seller_id', 'FAILED') == offers_data[i]['offer_reference']
    save_xml_response(offers_query_response.xml, 'query_offers_with_multiple_elements.xml')


# TODO Fix test_update_orders
# @pytest.mark.skip(reason='Waiting')
def test_update_orders(setup):
    # There are 3 orders:
    # * order 1 has 2 items
    # * order 2 has 3 items
    # * order 3 has 1 item

    manager = setup['manager']
    orders_query_response = manager.query_orders()

    orders_query_dict = orders_query_response.dict['orders_query_response']
    orders = orders_query_dict['order']
    order_ids = [order['order_id'] for order in orders]

    # Check the state of the order_id and if it hasn't been accepted yet, set
    # the action to 'Accepted'
    order1 = {}
    order1[order_ids[0]] = [{"order_detail_id": 1, "action": "Accepted"}, 
                            {"order_detail_id": 2, "action": "Accepted"}]
    order2 = {}
    order2[order_ids[1]] = [{"order_detail_id": 1, "action": "Refused"},
                            {"order_detail_id": 2, "action": "Refused"},
                            {"order_detail_id": 3, "action": "Refused"}
                            ]
    order3 = {}
    order3[order_ids[2]] = [{"order_detail_id": 1, "action": "Accepted"}]
    orders_update_response = manager.update_orders(order_ids[0], 'accept_order', order1[order_ids[0]])

    orders_update = [order1, order2, order3]
    orders_update_dict = orders_update_response.dict['orders_update_response']
    orders = orders_update_dict['order']
    
    if orders_update_dict['@status'] == 'OK':
        for i, order in enumerate(orders):
            assert orders[i].get('status') == 'OK'
            assert orders[i].get('state') == orders_update[i]['action']
    save_xml_response(orders_update_response.xml, 'update_orders.xml')
        

@pytest.mark.skip(reason='Waiting')
def test_query_orders(setup):
    """query_orders should return the orders placed by customers"""
    manager = setup['manager']
    orders_query_response = manager.query_orders()
    orders_query_dict = orders_query_response.dict['orders_query_response']
    orders = orders_query_dict['order']

    # We should have a list of orders
    assert isinstance(orders, (list, tuple))

    # There should be 3 orders
    assert len(orders) == 3

    # order 1 has 2 items
    assert isinstance(orders[0]['order_detail'], (list, tuple))
    assert len(orders[0]['order_detail']) == 2

    # order 2 has 3 items
    assert isinstance(orders[1]['order_detail'], (list, tuple))
    assert len(orders[1]['order_detail']) == 3

    # order 3 has 1 item
    assert isinstance(orders[2]['order_detail'], OrderedDict)

    # The elements in the order element should contain valid sub-elements
    assert all(x in ORDER_ELEMENTS for x in orders[0].keys())

    save_xml_response(orders_query_response.xml, 'query_orders.xml')


@pytest.mark.skip(reason='Waiting')
def test_query_pricing(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_query_batch(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_query_carriers(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_query_client_order_comments(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_query_messages(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_update_messages(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_query_incidents(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_update_incidents(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_query_shop_invoices(setup):
    pass
