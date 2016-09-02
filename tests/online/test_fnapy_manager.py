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

# Third-party modules
import pytest
import pytz

# Project modules
from fnapy.fnapy_manager import FnapyManager
from fnapy.utils import Response


# DATA
offer_data1 = {'product_reference':'0711719247159',
        'offer_reference':'B76A-CD5-153',
        'price':15, 'product_state':11, 'quantity':10, 
        'description': 'New product - 2-3 days shipping, from France'}

offer_data2 = {'product_reference':'5030917077418',
        'offer_reference':'B067-F0D-75E',
        'price':20, 'product_state':11, 'quantity':16, 
        'description': 'New product - 2-3 days shipping, from France'}

# SICP
offer_data3 = {'product_reference':'9780262510875',
        'offer_reference':'B76A-CD5-444',
        'price':80, 'product_state':11, 'quantity':10, 
        'description': 'New product - 2-3 days shipping, from France'}

# Batman V Superman L'aube de la justice 
offer_data4 = {'product_reference':'5051889562672',
        'offer_reference':'B067-F0D-444',
        'price':20, 'product_state':11, 'quantity':16, 
        'description': 'New product - 2-3 days shipping, from France'}

offers_data = [offer_data1, offer_data2, offer_data3, offer_data4]


@pytest.fixture
def setup():
    partner_id = os.environ.get('FNAC_PARTNER_ID')
    shop_id    = os.environ.get('FNAC_SHOP_ID')
    key        = os.environ.get('FNAC_KEY')
    from fnapy.connection import FnapyConnection
    connection = FnapyConnection(partner_id, shop_id, key)
    manager = FnapyManager(connection)
    manager.authenticate()
    # We make sure we always have the offers with the right values
    offers_update_response = manager.update_offers(offers_data)
    return {'manager': manager, 'response': offers_update_response}


# @pytest.mark.skip(reason='No waste of time')
def test_authenticate_returns_token(setup):
    """authenticate should return a token as a unicode"""
    token = setup['manager'].authenticate()
    assert isinstance(token, unicode)
    assert len(token) != 0


# @pytest.mark.skip(reason='No waste of time')
def test_update_offers(setup):
    """update_offers should return a response containing batch_id"""
    offers_update_dict = setup['response'].dict['offers_update_response']
    batch_id = offers_update_dict.get('batch_id')
    assert batch_id


# @pytest.mark.skip(reason='No waste of time')
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
# @pytest.mark.skip(reason='No waste of time')
def test_get_batch_status(setup):
    """get_batch_status should return a valid batch_status_response"""
    offers_update_response = setup['response']
    offers_update_dict = offers_update_response.dict['offers_update_response']
    batch_id = offers_update_dict.get('batch_id', '')
    batch_status_response = setup['manager'].get_batch_status(batch_id)
    batch_status_dict = batch_status_response.dict['batch_status_response']
    print batch_status_dict.get('@status')
    assert batch_status_dict.get('@status') == 'ACTIVE'


# @pytest.mark.skip(reason='No waste of time')
def test_query_offers_with_results_count(setup):
    """query_offers should return the first item when paging=1 and results_count=1"""
    offers_query_response = setup['manager'].query_offers(paging=1, results_count=1)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # The offers_query_response has an 'offer' element
    assert offers_query_dict .get('offer')
    assert int(offers_query_dict .get('nb_total_per_page', -1000)) == 1


# @pytest.mark.skip(reason='No waste of time')
def test_query_offers_with_a_single_parameter(setup):
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


# @pytest.mark.skip(reason='No waste of time')
def test_query_offers_with_multiple_parameters(setup):
    """query_offers should accept queries on multiple parameters"""
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


@pytest.mark.skip(reason='Waiting')
def test_update_orders(setup):
    pass


@pytest.mark.skip(reason='Waiting')
def test_query_orders(setup):
    pass


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
