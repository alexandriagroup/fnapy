#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Useful functions
"""

# Python modules
import os
import re
from codecs import open
from collections import OrderedDict

# Third-party modules
from lxml import etree
import xmltodict
import requests

# Project modules
from fnapy.config import *
from fnapy.compat import to_unicode
from fnapy.exceptions import FnapyUpdateOfferError


# CLASSES

class Query(object):
    """A simple class to create queries"""
    def __init__(self, name, tags={}, **kwargs):
        self._dict = OrderedDict()
        self.name = name
        self.attrib = kwargs

        for k, v in kwargs.items():
            if not k.startswith('@'):
                self._dict['@'+k] = v

        for k, v in tags.items():
            self._dict[k] = v

    def _create_new_dict(self):
        new_dict = OrderedDict()
        for k, v in self._dict.items():
            if k.startswith('@'):
                new_dict[k] = v
        return new_dict

    def was(self, state):
        """Perform a query on the states

        :state: the name of a state

        Example
        >>> states = Query('state').was('Created')

        """
        new_dict = self._create_new_dict()
        new_dict['state'] = {'#text': state}
        return Query(self.name, tags=new_dict)

    def between(self, min, max):
        new_dict = self._create_new_dict()
        new_dict['min'] = {'#text': min}
        new_dict['max'] = {'#text': max}
        return Query(self.name, tags=new_dict)

    def _operator(self, op, value):
        op_to_mode = {'eq': 'Equals',
                      'ge': 'GreaterThanOrEquals', 'gt': 'GreaterThan',
                      'le': 'LessThanOrEquals', 'lt': 'LessThan'} 
        new_dict = self._create_new_dict()
        new_dict['@mode'] = op_to_mode[op]
        new_dict['@value'] = value
        return Query(self.name, tags=new_dict)

    def eq(self, value):
        return self._operator('eq', value)

    def ge(self, value):
        return self._operator('ge', value)

    def gt(self, value):
        return self._operator('gt', value)

    def le(self, value):
        return self._operator('le', value)

    def lt(self, value):
        return self._operator('lt', value)

    @property
    def dict(self):
        """Return the OrderedDict"""
        return self._dict

    @property
    def xml(self):
        """Return the XML"""
        return dict2xml({self.name: self.dict})

    def __str__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.name)

    __repr__ = __str__


class HttpMessage(object):
    def __init__(self, content):
        # content is a string
        self.dict = xml2dict(content)

        # Raw XML
        self.xml = content

        # etree._Element
        self.element = etree.fromstring(self.xml)
        
        self.tag = re.sub(pattern='{[^}]+}', repl='', string=self.element.tag, flags=0)

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.tag)

    def __str__(self):
        return self.xml


class Request(HttpMessage):
    """A handy class to handle the request"""
    def __init__(self, content):
        super(Request, self).__init__(content)


class Response(HttpMessage):
    """A handy class to handle the response"""
    def __init__(self, content):
        super(Response, self).__init__(content)


# TODO Implement a check for the attributes
class Message(object):
    ACTIONS = (
        'mark_as_read', 'mark_as_unread', 'archive',
        'mark_as_read_and_archive', 'unarchive', 'reply', 'create'
    )

    TO = (
        'CALLCENTER', 'CLIENT', 'ALL'
    )

    SUBJECTS = (
        'product_information', 'shipping_information', 'order_information', 
        'offer_problem', 'offer_not_received', 'other_question'
    )

    TYPES = ('ORDER', 'OFFER')

    def __init__(self, action, id, to='ALL', description='', subject='', type='ORDER'): 
        self._action = action
        self._id = id
        self._to = to
        self._description = description
        self._subject = subject
        self._type = type

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, new_value):
        if new_value not in Message.ACTIONS:
            msg = 'Invalid action. Choose between {}.'.format(Message.ACTIONS)
            raise ValueError(msg)
        self._action = new_value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value):
        self._id = new_value

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, new_value):
        if new_value not in Message.TO:
            msg = 'Invalid recipient. Choose between {}.'.format(Message.TO)
            raise ValueError(msg)
        self._to = new_value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_value):
        self._description = new_value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, new_value):
        if new_value not in Message.SUBJECTS:
            msg = 'Invalid subject. Choose between {}'.format(Message.SUBJECTS)
            raise ValueError(msg)
        self._subject = new_value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_value):
        if new_value not in Message.TYPES:
            msg = 'Invalid type. Choose between {}'.format(Message.TYPES)
            raise ValueError(msg)
        self._type = new_value

    def __repr__(self):
        r = '<Message: action={self.action}, id={self.id}, to={self.to}, '
        r += 'description={self.description}, subject={self.subject}, '
        r += 'type={self.type}>'
        return r.format(self=self)

    def __str__(self):
        return """Message
action     : {self.action}
id         : {self.id}
to         : {self.to}
description: {self.description}
subject    : {self.subject}
type       : {self.type}
        """.format(self=self)

    def to_dict(self):
        """Return the a dictionary in the xmltodict format"""
        message = {'message': {
            '@action': self.action,
            '@id': self.id,
            'message_to': {'#text': self.to},
            'message_subject': {'#text': self.subject},
            'message_description': {'#text': self.description},
            'message_type': {'#text': self.type},
        }}
        return message


# FUNCTIONS
def get_url(sandbox=True):
    """Return the url for the sandbox or the real account

    Usage::
        url = get_url(sandbox=sandbox)

    :type sandbox: bool
    :param sandbox: determines whether you get the url for the sandbox
    account (True) or the real account (False).

    :rtype: str
    :returns: the entrypoint url to access the FNAC WebServices

    """
    use_sandbox = {True: "https://marketplace.ws.fd-recette.net/api.php/",
                   False: "https://vendeur.fnac.com/api.php/"}
    return use_sandbox[sandbox]


def get_credentials(sandbox=True):
    """Return the credentials for the sandbox or the real account

    Usage::
        credentials = get_credentials(sandbox=sandbox)

    :type sandbox: bool
    :param sandbox: determines whether you get the credentials for the sandbox
    account (True) or the real account (False).

    :rtype: dict
    :returns: the credentials for the selected account type
    
    """
    credentials = {
        'sandbox': {'partner_id': os.getenv('FNAC_SANDBOX_PARTNER_ID'),
                    'shop_id': os.getenv('FNAC_SANDBOX_SHOP_ID'),
                    'key': os.getenv('FNAC_SANDBOX_KEY')},
        'real': {'partner_id': os.getenv('FNAC_PARTNER_ID'),
                 'shop_id': os.getenv('FNAC_SHOP_ID'),
                 'key': os.getenv('FNAC_KEY')},
    }
    use_sandbox = {True: 'sandbox', False: 'real'}
    account_type = use_sandbox[sandbox]
    return credentials[account_type]


def dict2xml(_dict):
    """Returns a XML string from the input dictionary"""
    xml = xmltodict.unparse(_dict, pretty=True)
    xmlepured = remove_namespace(xml)
    return xmlepured


def remove_namespace(xml):
    """Remove the namespace from the XML string"""
    xmlepured = re.sub(pattern=' xmlns="[^"]+"', repl='', string=xml, flags=0)
    xmlepured = xmlepured.encode('utf-8')
    return xmlepured


def xpath(element, node_name):
    """A convenient function to look for nodes in the XML
    
    >>> nodes = xpath(response.element, node_name)

    """
    if '/' in node_name:
        node_name = '//ns:'.join(node_name.split('/'))
    return element.xpath('//ns:{0}'.format(node_name),
                         namespaces={'ns': XHTML_NAMESPACE})


def findall(element, node_name):
    """A convenient function to look for nodes in the XML
    
    >>> nodes = findall(response.element, node_name)

    """
    if '/' in node_name:
        node_name = '//ns:'.join(node_name.split('/'))
    return element.findall('.//ns:{0}'.format(node_name),
                         namespaces={'ns': XHTML_NAMESPACE})


def extract_text(element, node_name, index=0):
    """Extract the text from the selected node

    If many nodes are found, by default, the first one is chosen.
    You can change this by specifying the index=i where i is the nth
    element you want.
    If no text is found, the empty string is returned.

    """
    elements = xpath(element, node_name)
    if len(elements) > 0:
        text = elements[index].text
    else:
        text = ''
    return text


def xml2dict(xml):
    """Returns a dictionary from the input XML
    
    :type xml: unicode
    :param xml: The XML

    :rtype: dict
    :returns: the dictionary correspoding to the input XML
    """
    xmlepured = remove_namespace(to_unicode(xml))
    return xmltodict.parse(xmlepured)


def parse_xml(response, tag_name):
    """Get the text contained in the tag of the response

    :param response: the Response
    :param tag_name: the name of the tag
    :returns: the text enclosed in the tag
    
    """
    xml = etree.XML(response.content)
    return xml.xpath('//ns:token', namespaces={'ns':XHTML_NAMESPACE})[0].text


def check_offer_data(offer_data):
    """Check the offer_data passed to update_offers is valid
    
    :type offer_data: dict
    :param offer_data: the parameters used to update an offer

    :returns: None

    offer_data must be a dictionary with at least 2 keys:
    - offer_reference (the sku)
    - any other parameter allowed by the service (price, quantity,
    product_state, ...)

    Raises a FnapyUpdateOfferError if the offer_data is not valid.

    """
    if not isinstance(offer_data, dict):
        msg = 'The argument must be a dictionary.'
        raise FnapyUpdateOfferError(msg)

    if 'offer_reference' not in offer_data:
        msg = 'The dictionary must contain the key "offer_reference" (the sku)'
        raise FnapyUpdateOfferError(msg)

    valid_keys = [x.name for x in REQUEST_ELEMENTS['offers_update']]
    for key in offer_data:
        if key not in valid_keys:
            msg = '{0} is not a valid parameter for updating an offer. '
            msg += ' Choose amongst {1}'
            msg = msg.format(key, valid_keys)
            raise FnapyUpdateOfferError(msg)

# TODO Reimplement create_offer_element with kwargs
def create_offer_element(offer_data):
    """Create an offer element

    An offer needs at least one offer_reference (SKU) and any other parameter
    accepted by the service (cf documentation)
    :param offer_reference: a seller offer reference (such as SKU)
    :param product_reference: a product reference (such as EAN)
    :param product_state: a product state
    :param price: a price
    :param quantity: a quantity
    :param description: a description of the product

    :returns: offer (etree.Element)

    """
    offer = etree.Element('offer')
    offer_reference = offer_data['offer_reference']
    etree.SubElement(offer, "offer_reference", type="SellerSku").text = etree.CDATA(offer_reference)
    offer_data_items = [(k, v) for k, v in offer_data.items() if k != 'offer_reference']

    for key, value in offer_data_items:
        if key == 'product_reference':
            etree.SubElement(offer, 'product_reference', type="Ean").text = str(value)
        elif key == 'description':
            etree.SubElement(offer, 'description').text = etree.CDATA(value)
        else:
            etree.SubElement(offer, key).text = str(value)
    return offer


def create_xml_element(connection, token, name):
    """A helper function creating an etree.Element with the necessary
    attributes

    :param name: The name of the element
    :returns: etree.Element

    """
    return etree.Element(name, nsmap={None: XHTML_NAMESPACE},
            shop_id=connection.shop_id, partner_id=connection.partner_id, token=token)


def get_order_ids(orders_query_response):
    """Returns the order_ids in orders_query_response"""
    orders = orders_query_response.dict['orders_query_response'].get('order', None)
    order_ids = []
    if orders:
        if isinstance(orders, (list, tuple)):
            for order in orders:
                order_ids.append(order.get('order_id', ''))
        elif isinstance(orders, dict):
            order_ids.append(orders.get('order_id', ''))
    return order_ids


def get_token(sandbox=True):
    # We use the real seller account
    credentials = get_credentials(sandbox)
    partner_id = credentials['partner_id']
    shop_id = credentials['shop_id']
    key = credentials['key']

    xml = """<?xml version="1.0" encoding="utf-8"?>
<auth xmlns='http://www.fnac.com/schemas/mp-dialog.xsd'>
  <partner_id>{partner_id}</partner_id>
  <shop_id>{shop_id}</shop_id>
  <key>{key}</key>
</auth>
    """.format(partner_id=partner_id, shop_id=shop_id, key=key)
    url = get_url(sandbox)
    response = post(url, 'auth', xml)
    return parse_xml(response, 'token')


def set_credentials(xml, sandbox=True):
    """Set the credentials in the given raw XML """
    credentials = get_credentials(sandbox)
    creds = {'shop_id': credentials['shop_id'],
             'partner_id': credentials['partner_id'],
             'token': get_token(sandbox)}

    for cred, value in creds.items():
        xml = re.sub(pattern='{0}="[^"]+"'.format(cred),
                     repl='{0}="{1}"'.format(cred, value), string=xml, flags=0)
    return xml


def post(url, service, request):
    request = to_unicode(request).encode('utf-8')
    return requests.post(url + service, request, headers=HEADERS)


def save_xml_response(response, action):
    """Save the response in a file """
    output_dir = os.path.dirname(os.path.abspath(__file__))
    filename = action + '_response.xml'
    with open(os.path.join(output_dir, '../tests/assets', filename), 'w') as f:
        f.write(response.encode('utf-8'))
        print('Saved the response in {}'.format(filename))    


def load_xml_request(action):
    input_dir = os.path.dirname(os.path.abspath(__file__))
    filename = action + '_request.xml'
    with open(os.path.join(input_dir, '../tests/assets', filename), 'r', 'utf-8') as f:
        request = f.read()
    return request
