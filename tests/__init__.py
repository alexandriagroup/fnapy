# coding: utf-8

# Python
from __future__ import unicode_literals, print_function
import os
from codecs import open
from contextlib import contextmanager

# Third-party
from requests import Response
import pytest

# Project
from fnapy.fnapy_manager import FnapyManager
from fnapy.connection import FnapyConnection


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


# FUNCTIONS
def save_xml_response(response, filename):
    """Save the response in a file """
    output_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(output_dir, 'offline/assets', filename), 'w') as f:
        f.write(response.encode('utf-8'))
        print('Saved the response in {}'.format(filename))    


# TODO Use mock instead of sending request to the server
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


@pytest.fixture
def fake_manager(monkeypatch):
    monkeypatch.setattr('requests.post', make_requests_get_mock('authenticate.xml'))
    partner_id = os.environ.get('FNAC_PARTNER_ID')
    shop_id    = os.environ.get('FNAC_SHOP_ID')
    key        = os.environ.get('FNAC_KEY')
    connection = FnapyConnection(partner_id, shop_id, key)
    manager = FnapyManager(connection)
    manager.authenticate()
    return manager


def make_requests_get_mock(filename):
    def mockreturn(*args, **kwargs):
        response = Response()
        with open(os.path.join(os.path.dirname(__file__), 'offline/assets', filename), 'r', 'utf-8') as fd:
            response._content = fd.read().encode('utf-8')
        return response
    return mockreturn


def make_simple_text_mock(filename):
    def mockreturn(*args, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), 'offline/assets', filename), 'r', 'utf-8') as fd:
            return fd.read()
    return mockreturn


@contextmanager
def assert_raises(exception_class, msg=None):
    """Check that an exception is raised and its message contains `msg`."""
    with pytest.raises(exception_class) as exception:
        yield
    if msg is not None:
        message = '%s' % exception
        assert msg.lower() in message.lower()
