# coding: utf-8

# Python
from __future__ import unicode_literals, print_function
import os
import re
from copy import copy
from codecs import open
from contextlib import contextmanager

# Third-party
import requests
from lxml import etree
import pytest

# Project
from fnapy.fnapy_manager import FnapyManager
from fnapy.connection import FnapyConnection
from fnapy.utils import *


# sandbox is False means real account.
SANDBOX = True

# DATA
offer_data1 = {'product_reference':'0711719247159',
        'offer_reference':'B76A-CD5-153',
        'price':15, 'product_state':11, 'quantity':10, 
        'description': 'New product - 2-3 days shipping, from France'}

offer_data2 = {'product_reference':'5030917077418',
        'offer_reference':'B067-F0D-75E',
        'price':20, 'product_state':11, 'quantity':16, 
        'description': 'New product - 2-3 days shipping, from France'}

offer_data3 = {'product_reference': '5051889022091',
               'offer_reference': '561C-385-9BE',
               'price': 10.55, 'product_state': 11, 'quantity': 16,
               'description': 'New product - Blu-ray disc - 2-3 days shipping, from France'}

# # SICP
# offer_data3 = {'product_reference':'9780262510875',
#         'offer_reference':'B76A-CD5-444',
#         'price':80, 'product_state':11, 'quantity':10, 
#         'description': 'New product - 2-3 days shipping, from France'}

# # Batman V Superman L'aube de la justice 
# offer_data4 = {'product_reference':'5051889562672',
#         'offer_reference':'B067-F0D-444',
#         'price':20, 'product_state':11, 'quantity':16, 
#         'description': 'New product - 2-3 days shipping, from France'}

offers_data = [offer_data1, offer_data2, offer_data3]

# invalid offer_data is offer_data1 without offer_reference
invalid_offer_data = copy(offer_data1)
del invalid_offer_data['offer_reference']
invalid_offers_data = [offer_data1, invalid_offer_data]


# FUNCTIONS
@pytest.fixture
def setup():
    from fnapy.connection import FnapyConnection
    connection = FnapyConnection(sandbox=SANDBOX)
    manager = FnapyManager(connection)
    manager.authenticate()
    # We make sure we always have the offers with the right values
    offers_update_response = manager.update_offers(offers_data)
    return {'manager': manager, 'response': offers_update_response}


def get_fake_credentials(*args, **kwargs):
    return {'partner_id': 'XXX', 'shop_id': 'XXX', 'key': 'XXX', 'sandbox': 0}

@pytest.fixture
def fake_manager(monkeypatch):
    """Create a manager that doesn't need to connect to the server to get a token"""
    # We mock the request to the authentication web service in FnapyManager
    monkeypatch.setattr('requests.post',
                        make_requests_get_mock('auth_response.xml'))
    # We mock get_crendentials so that we don't have to provide environment
    # variables
    monkeypatch.setattr('fnapy.connection.get_credentials', get_fake_credentials)

    # We mock the check of the credentials in FnapyConnection
    # so that we can initiate the connection with any credentials
    monkeypatch.setattr('fnapy.connection.check_credentials_validity',
                        lambda x: None)
    connection = FnapyConnection(sandbox=True)
    manager = FnapyManager(connection)
    manager.authenticate()
    return manager


def make_requests_get_mock(filename):
    def mockreturn(*args, **kwargs):
        response = requests.Response()
        with open(os.path.join(os.path.dirname(__file__), 'assets', filename), 'r', 'utf-8') as fd:
            response._content = fd.read().encode('utf-8')
        return response
    return mockreturn


@contextmanager
def assert_raises(exception_class, msg=None):
    """Check that an exception is raised and its message contains `msg`."""
    with pytest.raises(exception_class) as exception:
        yield
    if msg is not None:
        message = '%s' % exception
        assert msg.lower() in message.lower()


def sorted_elements(root):
    new_root = etree.Element(root.tag, attrib=root.attrib)
    new_root.text = root.text
    for e in sorted(root.getchildren(), key=lambda x: x.tag):
        element = etree.Element(e.tag, attrib=e.attrib)
        element.text = e.text
        new_root.append(element)
    return new_root


def elements_are_equal(e1, e2, excluded_attrs=[]):
    e1 = sorted_elements(e1)
    e2 = sorted_elements(e2)

    if e1.tag != e2.tag:
        return False

    if e1.text is not None and e2.text is not None and\
       e1.text.strip() != e2.text.strip():
        return False

    if e1.tail != e2.tail:
        return False

    if excluded_attrs:
        if {v for k, v in e1.attrib.items() if k not in excluded_attrs} !=\
           {v for k, v in e2.attrib.items() if k not in excluded_attrs}:
            return False
    else:
        if e1.attrib != e2.attrib:
            return False

    if len(e1) != len(e2):
        return False

    return all(elements_are_equal(c1, c2) for c1, c2 in zip(e1, e2))


def xml_contains_error(xml_dict):
    """Return True if one key is 'error'"""
    return 'error' in xml_dict


def xml_is_valid(xml_dict, xml_valid_keys):
    """Return True if all the keys in the XML dictionary are valid"""
    if len(xml_dict) == 0:
        return False, 'The XML dictionary is empty.'
    keys = [tag for tag in xml_dict.keys() if not tag.startswith('@')]
    if len(keys) == 0:
        return False, 'The XML dictionary contains no valid keys.'
    invalid_keys = set(keys).difference((x.name for x in xml_valid_keys))
    result = len(invalid_keys) == 0
    if result:
        return True, ''
    else:
        msg = 'The XML has the following invalid keys {}'.format(invalid_keys)
        if len(invalid_keys) == 1 and 'error' in invalid_keys:
            print(xml_dict['error'])
        return False, msg


def response_is_valid(action, service):
    """The response is valid if it contains the elements defined in the API"""
    request = load_xml_request(action) 
    request = set_credentials(request, sandbox=SANDBOX)
    url = get_url(sandbox=SANDBOX)
    response = post(url, service, request).text
    xml_dict = xml2dict(response).get(service + '_response', {})
    result, error = xml_is_valid(xml_dict, RESPONSE_ELEMENTS[service])
    if result:
        save_xml_response(response, action)
    elif result is False:
        pytest.fail(error)
    return result


def response_is_not_valid(action, service):
    """The request is not valid if an 'error' node is in the response"""
    request = load_xml_request(action)
    request = set_credentials(request, sandbox=SANDBOX)
    url = get_url(sandbox=SANDBOX)
    response = post(url, service, request).text
    xml_dict = xml2dict(response).get(service + '_response', {})
    result = xml_contains_error(xml_dict)
    if result:
        save_xml_response(response, action)
    elif result is False:
        pytest.fail("The XML doesn't contain the error node")
    return result


def request_is_valid(request, action, service):
    """The request is valid if it contains the same information as in the valid XML request file"""
    expected = load_xml_request(action)
    expected_element = etree.XML(expected.encode('utf-8'))
    request_element = request.element
    credentials = ('partner_id', 'shop_id', 'token')
    result = elements_are_equal(request_element, expected_element, credentials)
    if not result:
        pytest.fail('Invalid request:\n{0}\nshould be:\n{1}'.format(request.xml, expected))
    return result
