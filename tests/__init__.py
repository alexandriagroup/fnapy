# coding: utf-8

# Python
from __future__ import unicode_literals, print_function
import os
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
# Motor Storm
offer_data1 = {'product_reference': '0711719247159',
               'offer_reference': 'B76A-CD5-153',
               'price': 15, 'product_state': 11, 'quantity': 10,
               'description': 'New product - 2-3 days shipping, from France'}

# Mordern Warfare 2
offer_data2 = {'product_reference': '5030917077418',
               'offer_reference': 'B067-F0D-75E',
               'price': 20, 'product_state': 11, 'quantity': 16,
               'description': 'New product - 2-3 days shipping, from France'}

# The Dark Knight 
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


def gettext(node):
    text = node.text.strip() if node.text else None
    return text if text else None


def error_msg(name, n1, n2, x1, x2):
    """
    Generate an error message notifying the different values x1 and x2
    in the nodes n1 and n2.
    """
    return 'Different {name} in\n{n1}\nand\n{n2}:\n> {x1} != {x2}'.format(
        name=name, n1=etree.tostring(n1).decode('utf8'),
        n2=etree.tostring(n2).decode('utf8'), x1=x1, x2=x2
    )


def nodes_are_equal(n1, n2, excluded_attrs=[]):
    # Attributes
    if excluded_attrs:
        attribs1 = {(k, v) for k, v in n1.items() if k not in excluded_attrs}
        attribs2 = {(k, v) for k, v in n2.items() if k not in excluded_attrs}
        if len(attribs1.symmetric_difference(attribs2)) > 0:
            return False, error_msg('attributes', n1, n2, attribs1, attribs2)
    # Text
    if gettext(n1) != gettext(n2):
        return False, error_msg('text', n1, n2, gettext(n1), gettext(n2))

    return True, None


def elements_are_equal(e1, e2, excluded_attrs=[]):
    nodes1 = sorted(e1.getiterator(), key=lambda e: e.tag)
    nodes2 = sorted(e2.getiterator(), key=lambda e: e.tag)
    tags1 = [x.tag for x in nodes1]
    tags2 = [x.tag for x in nodes2]

    if tags1 != tags2:
        return False, error_msg('tags', e1, e2, tags1, tags2)

    for node1, node2 in zip(nodes1, nodes2):
        result, error = nodes_are_equal(node1, node2)
        if result is False:
            return False, error
    return True, None


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
    result, error = elements_are_equal(request_element, expected_element, credentials)
    if error:
        # pytest.fail('Invalid request:\n{0}\nshould be:\n{1}'.format(request.xml, expected))
        pytest.fail(error)
    return result
