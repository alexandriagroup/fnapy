# Python modules
from __future__ import unicode_literals
import os
from datetime import datetime
from contextlib import closing

# Third-party modules
import pytest
import pytz

# Project modules
from fnapy.fnapy_manager import FnapyManager
from tests import make_requests_get_mock, fake_manager, offers_data,\
request_is_valid
from tests.offline import ContextualTest


def test_query_offers(monkeypatch, fake_manager):
    context = ContextualTest(monkeypatch, fake_manager, 'query_offers', 'offers_query')
    with closing(context):
        dmin = datetime(2016, 8, 23, 0, 0, 0).replace(tzinfo=pytz.utc)
        dmax = datetime(2016, 8, 31, 0, 0, 0).replace(tzinfo=pytz.utc)
        date = {'@type': 'Created',
                'min': { "#text": dmin.isoformat() },
                'max': { "#text": dmax.isoformat() }
                }
        fake_manager.query_offers(results_count=100, date=date)


def test_update_offers(monkeypatch, fake_manager):
    context = ContextualTest(monkeypatch, fake_manager, 'update_offers', 'offers_update')
    with closing(context):
        fake_manager.update_offers(offers_data)


def test_get_batch_status(monkeypatch, fake_manager):
    context = ContextualTest(monkeypatch, fake_manager, 'get_batch_status', 'batch_status')
    with closing(context):
        fake_manager.get_batch_status('5D239E08-F6C1-8965-F2FA-7EFCC9E7BAD1')


@pytest.mark.skip(reason='More advanced tests')
def test_query_offers_with_results_count(monkeypatch, fake_manager):
    """query_offers should return the first item when paging=1 and results_count=1"""
    monkeypatch.setattr('requests.post', make_requests_get_mock('query_offers_with_results_count.xml'))
    offers_query_response = fake_manager.query_offers(paging=1, results_count=1)
    offers_query_dict = offers_query_response.dict['offers_query_response']

    # The offers_query_response has an 'offer' element
    assert offers_query_dict.get('offer')
    assert int(offers_query_dict.get('nb_total_per_page', -1000)) == 1


@pytest.mark.skip(reason='More advanced tests')
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


@pytest.mark.skip(reason='More advanced tests')
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


