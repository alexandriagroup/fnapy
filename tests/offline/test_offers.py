# Python modules
from __future__ import unicode_literals
import os
from datetime import datetime

# Third-party modules
import pytest
import pytz

# Project modules
from fnapy.fnapy_manager import FnapyManager
from tests import make_requests_get_mock, fake_manager,\
    offers_data, invalid_offers_data, request_is_valid
from tests.offline import create_context_for_requests
from fnapy.utils import Query
from fnapy.exceptions import FnapyUpdateOfferError

dmin = datetime(2016, 8, 23, 0, 0, 0).replace(tzinfo=pytz.utc).isoformat()
dmax = datetime(2016, 8, 31, 0, 0, 0).replace(tzinfo=pytz.utc).isoformat()

def test_query_offers(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager, 'query_offers', 'offers_query')
    with context:
        date = Query('date', type='Created').between(min=dmin, max=dmax)
        fake_manager.query_offers(results_count=100, date=date)


def test_update_offers(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager, 'update_offers', 'offers_update')
    with context:
        fake_manager.update_offers(offers_data)


def test_update_offers_without_offer_reference(monkeypatch, fake_manager):
    with pytest.raises(FnapyUpdateOfferError):
        fake_manager.update_offers(invalid_offers_data)


def test_get_batch_status(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager, 'get_batch_status', 'batch_status')
    with context:
        fake_manager.get_batch_status('5D239E08-F6C1-8965-F2FA-7EFCC9E7BAD1')


def test_query_offers_with_multiple_parameters(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                             'query_offers_with_multiple_parameters', 'offers_query')
    with context:
        date = Query('date', type='Created').between(min=dmin, max=dmax)
        quantity = Query('quantity').eq(10)
        fake_manager.query_offers(results_count=100, date=date,
                                  quantity=quantity)


def test_delete_offers(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'delete_offers', 'offers_update')
    with context:
        fake_manager.update_offers(offers_data)
        # Then we delete 2
        offer_references = [x['offer_reference'] for x in offers_data[:2]]
        fake_manager.delete_offers(offer_references)


