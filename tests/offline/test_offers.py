# Python modules
from __future__ import unicode_literals
import os
from datetime import datetime

# Third-party modules
import pytest
import pytz

# Project modules
from fnapy.fnapy_manager import FnapyManager
from tests import make_requests_get_mock, fake_manager, offers_data


def test_update_offers(monkeypatch, fake_manager):
    """update_offers should return a batch_id"""
    monkeypatch.setattr('requests.post', make_requests_get_mock('update_offers.xml'))
    offers_update_response = fake_manager.update_offers([offers_data[0]])
    offers_update_dict = offers_update_response.dict['offers_update_response']
    batch_id = offers_update_dict.get('batch_id')
    assert batch_id


def test_get_batch_status(monkeypatch, fake_manager):
    """get_batch_status should return a valid batch_status_response"""
    monkeypatch.setattr('requests.post', make_requests_get_mock('update_offers.xml'))
    offers_update_response = fake_manager.update_offers(offers_data)
    offers_update_dict = offers_update_response.dict['offers_update_response']
    batch_id = offers_update_dict.get('batch_id', '')
    monkeypatch.setattr('requests.post', make_requests_get_mock('get_batch_status.xml'))
    batch_status_response = fake_manager.get_batch_status(batch_id)
    batch_status_dict = batch_status_response.dict['batch_status_response']
    assert batch_status_dict.get('@status') == 'ACTIVE'


def test_query_offers_with_results_count(monkeypatch, fake_manager):
    """query_offers should return the first item when paging=1 and results_count=1"""
    monkeypatch.setattr('requests.post', make_requests_get_mock('query_offers_with_results_count.xml'))
    offers_query_response = fake_manager.query_offers(paging=1, results_count=1)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # The offers_query_response has an 'offer' element
    assert offers_query_dict.get('offer')
    assert int(offers_query_dict.get('nb_total_per_page', -1000)) == 1


def test_query_offers_with_single_prameter(monkeypatch, fake_manager):
    """query_offers should accept a single parameter"""
    monkeypatch.setattr('requests.post', make_requests_get_mock('query_offers_with_single_element.xml'))
    offer_count_expected = 2
    quantity = {'@mode': 'Equals', '@value': 16}
    offers_query_response = fake_manager.query_offers(quantity=quantity)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # Only 2 offers whose quantity = 16
    offers = offers_query_dict.get('offer', [])
    assert len(offers) == offer_count_expected

    # The offer_seller_id should be the SKU (offer_reference) of the offers
    # with the corresponding criteria
    for i in range(offer_count_expected):
         offers[i].get('offer_seller_id', 'FAILED') == offers_data[i]['offer_reference']


def test_query_offers_with_multiple_elements(monkeypatch, fake_manager):
    """query_offers should accept queries on multiple elements"""
    monkeypatch.setattr('requests.post', make_requests_get_mock('query_offers_with_multiple_elements.xml'))
    offer_count_expected = 2
    dmin = datetime(2016, 8, 23, 0, 0, 0).replace(tzinfo=pytz.utc)
    dmax = datetime(2016, 9, 2, 0, 0, 0).replace(tzinfo=pytz.utc)
    date = {'@type': 'Modified',
            'min': {'#text': dmin.isoformat()},
            'max': {'#text': dmax.isoformat()}
            }
    quantity = {'@mode': 'Equals', '@value': 16}
    offers_query_response = fake_manager.query_offers(quantity=quantity, date=date)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # Only 2 offers whose quantity = 16 and within the given time range
    offers = offers_query_dict.get('offer', [])
    assert len(offers) == offer_count_expected

    # The offer_seller_id should be the SKU (offer_reference) of the offers
    # with the corresponding criteria
    for i in range(offer_count_expected):
        offers[i].get('offer_seller_id', 'FAILED') == offers_data[i]['offer_reference']


