#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Manage your offers on the FNAC marketplace
"""

# Third-party modules
import requests

# Project modules
from utils import *
from config import *


class FnapyManager(object):
    """A class to manage your offers"""
    def __init__(self, connection):
        """Initialize the """
        self.connection = connection
        self.offers_update_request = None
        self.offers_query_request = None
        self.orders_update_request = None
        self.pricing_query_request = None
        self.carriers_query_request = None
        self.batch_status_request = None
        self.messages_query_request = None
        self.messages_update_request = None
        self.shop_invoices_query_request = None
        self.incidents_query_request = None
        self.incidents_update_request = None

        # The batch_id updated every time an offer is updated
        self.batch_id = None

    def _get_response(self, element, xml):
        """Send the request and return the response as a dictionary

        :type element: lxml.etree.Element
        :param element: the XML element
        
        :type xml: str
        :param xml: the XML string sent in the request

        :rtype: Response
        :returns: response
        """
        service = element.tag
        response = requests.post(URL + service, xml, headers=HEADERS)
        response = Response(response.text)
        if response.dict.get(service + '_response', {}).get('error'):
            print 'The token expired. Reauthenticating...'
            # Reauthenticate and update the element
            element.attrib['token'] = self.authenticate()
            setattr(self, service + '_request', etree.tostring(element, **XML_OPTIONS)) 
            # Resend the updated request
            response = requests.post(URL + service, getattr(self, service + '_request'), headers=HEADERS)
            response = Response(response.text)
        return response

    def authenticate(self):
        """Authenticate to the FNAC API and return a token"""
        auth = etree.Element('auth', nsmap={None: XHTML_NAMESPACE})
        etree.SubElement(auth, 'partner_id').text = self.connection.partner_id
        etree.SubElement(auth, 'shop_id').text = self.connection.shop_id
        etree.SubElement(auth, 'key').text = self.connection.key
        auth_request = etree.tostring(auth, **XML_OPTIONS)
        response = requests.post(URL + 'auth', auth_request, headers=HEADERS)
        self.token = parse_xml(response, 'token')
        return self.token

    def update_offers(self, offers_data, token=None):
        """Post the update offers and return the response

        Usage:
        >>> response = manager.update_offers(offers_data, token=token)
        
        :param offers_data: the list of data to create the offers
        :param token: the token returned by the server

        :rtype: Response
        :returns response: the offers_update_response dictionary

        """
        if token is not None:
            self.token = token

        offers_update = create_xml_element(self.connection, self.token, 'offers_update')
        for offer_data in offers_data:
            offer = create_offer_element(**offer_data)
            offers_update.append(offer)
        self.offers_update_request = etree.tostring(offers_update, **XML_OPTIONS)

        # the response contains the element batch_id
        response = self._get_response(offers_update, self.offers_update_request)
        self.batch_id = response.dict['offers_update_response']['batch_id']
        return response

    # TODO Improve the documentation
    def update_orders(self, order_id, order_update_action, actions):
        """Update the selected order with an order_update_action

        Usage:
        >>> response = manager.update_orders(order_id, order_update_action, actions)

        where `order_update_action` is a list of dictionaries with 2 keys
        'order_detail_id' and 'action'.
        order_detail_id designates the id of an item in a given order
        (designated itself by order_id).

        Available order_update_action:
        * accept_order       : The action for the order is accepting orders by the
                               seller
        * confirm_to_send    : The action for the order is confirming sending
                               orders by the seller
        * update             : The action for the order is updating orders by the seller
        * accept_all_orders  : The action for the order is accepting or refusing
                               all order_details of the order by the seller
        * confirm_all_to_send: The action for the order is confirming sending
                               all order_details by the seller
        * update_all         : The action for the order is to update tracking
                               information for all order_details

        Example: Accept the first item and refuse the second
        >>> action1 = {"order_detail_id": 1, "action": "Accepted"}
        >>> action2 = {"order_detail_id": 2, "action": "Refused"}
        >>> response = update_orders("LDJEDEAS123", [action1, action2])

        """
        order_id = str(order_id)
        orders_update = create_xml_element(self.connection, self.token, 'orders_update')
        order = etree.Element('order', order_id=order_id,
                action=order_update_action)

        for action in actions:
            order_detail = etree.Element("order_detail")
            etree.SubElement(order_detail, 'order_detail_id').text = str(action['order_detail_id'])
            etree.SubElement(order_detail, 'action').text = str(action['action'])
            order.append(order_detail)

        orders_update.append(order)
        self.orders_update_request = etree.tostring(orders_update, **XML_OPTIONS)
        return self._get_response(orders_update, self.orders_update_request)

    # FIXME The batch_status_response doesn't contain the attributes (status)
    def get_batch_status(self, batch_id=None, token=None):
        """Return the status for the given batch id

        :param conn: The FnapyConnection instance
        :param batch_id: the batch id
        :rtype: Response
        :returns: batch status response

        """
        if token is not None:
            self.token = token

        if batch_id is not None:
            self.batch_id = batch_id

        batch_status = create_xml_element(self.connection, self.token, 'batch_status')
        etree.SubElement(batch_status, 'batch_id').text = self.batch_id
        self.batch_status_request = etree.tostring(batch_status, **XML_OPTIONS)
        return self._get_response(batch_status, self.batch_status_request)

    # TODO Implement this method that should handle any arguments to create
    # the xml properly
    def _check_elements(self, valid_elements, selected_elements):
        for element in selected_elements:
            if element not in valid_elements:
                raise ValueError('{} is not a valid element.'.format(element))

    def _query(self, query_type, results_count='100', token=None, **elements):
        """Query your catalog and return the {query_type} on the selected page between 2 datetimes

        Usage:
        >>> response = manager.query_offers(results_count=results_count, token=token)

        Example:
        Find the {query_type} created between 2 dates
        >>> response = manager.query_offers(date={'@type': 'Modified',
                'min': {'#text': "2016-08-23T17:00:00+00:00"},
                'max': {'#text': "2016-08-26T17:00:00+00:00"}}
                )

        Find the 2 first items  of the catalog
        >>> response = manager.query_offers(results_count=2)

        :param token: the token returned by the server (optional)

        :rtype: Response
        :returns: the response

        """
        print 'Querying {}...'.format(query_type)
        if token is not None:
            self.token = token

        valid_query_types = ('offers', 'orders', 'client_order_comments',
                             'messages', 'incidents', 'shop_invoices')
        if query_type in valid_query_types:
            query_type += "_query"
        else:
            raise ValueError("The query_type must be in {}".format(valid_query_types))

        # Check the queried elements
        if query_type == 'offers_query':
            self._check_elements(OFFERS_QUERY_ELEMENTS, elements.keys())
        elif query_type == 'orders_query':
            self._check_elements(ORDERS_QUERY_ELEMENTS, elements.keys())
        elif query_type == 'client_order_comments_query':
            self._check_elements(CLIENT_ORDER_COMMENTS_QUERY_ELEMENTS, elements.keys())
        elif query_type == 'messages_query':
            self._check_elements(MESSAGES_QUERY_ELEMENTS, elements.keys())
        elif query_type == 'incidents_query':
            self._check_elements(INCIDENTS_QUERY_ELEMENTS, elements.keys())
        elif query_type == 'shop_invoices_query':
            self._check_elements(SHOP_INVOICES_QUERY_ELEMENTS, elements.keys())

        # Make sure we have unicode
        # paging = str(paging).decode('utf-8')
        results_count = str(results_count).decode('utf-8')

        # Create the XML element
        query = create_xml_element(self.connection, self.token, query_type)
        query.attrib['results_count'] = results_count

        # Create the XML from the queried elements 
        if len(elements):
            queried_elements = etree.XML(dict2xml(elements))
            query.append(queried_elements)

        setattr(self, query_type + '_request', etree.tostring(query, **XML_OPTIONS))
        query_xml = getattr(self, query_type + '_request')
        return self._get_response(query, query_xml)

    # TODO generator for the paging
    # TODO Allow to specify the type of date ('Created', 'Modified'...)
    def query_offers(self, results_count='100', token=None, **elements):
        return self._query('offers', results_count, token=token, **elements)

    def query_orders(self, results_count='100', token=None, **elements):
        return self._query('orders', results_count, token=token, **elements)

    def query_pricing(self, ean, sellers="all"):
        """Compare price between all marketplace shop and fnac for a specific product (designated by its ean)

        Usage:
        >>> response = manager.query_pricing(ean, sellers=sellers)

        :rtype: Response
        :returns: response

        """
        pricing_query = create_xml_element(self.connection, self.token, 'pricing_query')
        pricing_query.attrib['sellers'] = sellers
        product_reference = etree.Element("product_reference", type="Ean")
        product_reference.text = str(ean)
        pricing_query.append(product_reference)
        self.pricing_query_request = etree.tostring(pricing_query, **XML_OPTIONS)
        return self._get_response(pricing_query, self.pricing_query_request)

    def query_batch(self):
        """Return information about your currently processing import batches

        Usage:
        >>> response = manager.query_batch()

        :rtype: Response
        :returns: response

        """
        batch_query = create_xml_element(self.connection, self.token, 'batch_query')
        self.batch_query_request = etree.tostring(batch_query, **XML_OPTIONS)
        return self._get_response(batch_query, self.batch_query_request)

    def query_carriers(self):
        """Return the available carriers managed on FNAC Marketplace platform
        
        Usage:
        >>> response = manager.query_carriers()

        :rtype: Response
        :returns: response

        """
        carriers_query = create_xml_element(self.connection, self.token, 'carriers_query')
        etree.SubElement(carriers_query, "query").text = etree.CDATA("all")
        self.carriers_query_request = etree.tostring(carriers_query, **XML_OPTIONS)
        return self._get_response(carriers_query, self.carriers_query_request)

    def query_client_order_comments(self, results_count='100', token=None, **elements):
        """Retrieves customers comments and ratings about your orders.

        Usage
        >>> response = manager.query_client_order_comments(results_count=results_count,\
                                                        token=token, **elements)

        :rtype: Response
        :returns: response

        """
        return self._query('client_order_comments', results_count, token=token, **elements)

    def update_client_order_comments(self, seller_comment, offer_fnac_id):
        """Reply to client order comments

        Usage
        >>> response = manager.update_client_order_comments(comment)

        :rtype: Response
        :returns: response

        """
        client_order_comments_update = create_xml_element(self.connection, self.token,
                                                          'client_order_comments_update')
        comment = etree.Element('comment', id=offer_fnac_id)
        etree.SubElement(comment, 'comment_reply').text = etree.CDATA(seller_comment)
        client_order_comments_update.append(comment)
        self.client_order_comments_update_request = etree.tostring(client_order_comments_update, **XML_OPTIONS)
        return self._get_response(client_order_comments_update,
                self.client_order_comments_update_request)

    def query_messages(self, results_count='100', token=None, **elements):
        """Return the messages related to your orders or offers

        Usage
        >>> response = manager.query_messages(results_count=results_count,
        token=token, **elements)

        :rtype: Response
        :returns: response

        """
        return self._query('messages', results_count, token=token, **elements)

    def update_messages(self, messages):
        """Update message sent on your offers or orders : reply, set as read, ...

        Usage
        >>> response = manager.update_messages(messages)

        :type messages: Message
        :param messages: the specified messages we want to update

        :rtype: Response
        :returns: response

        Example
        >>> m1 = Message(action='mark_as_read', id='12345')
        >>> m2 = Message(action='reply', id='12345')
        >>> m2.description = 'Your order has been shipped'
        >>> m2.subject = 'order_information'
        >>> m2.type = 'ORDER'
        >>> response = manager.update_messages([m1, m2])

        """
        messages_update = create_xml_element(self.connection, self.token, 'messages_update')
        for m in messages:
            message = etree.XML(dict2xml(m.to_dict()))
            messages_update.append(message)

        self.messages_update_request = etree.tostring(messages_update, **XML_OPTIONS)
        return self._get_response(messages_update, self.messages_update_request)

    def query_incidents(self, results_count='100', token=None, **elements):
        """Return the incidents related to your orders

        Usage
        >>> response = manager.query_incidents(results_count=results_count,
        token=token, **elements)

        :rtype: Response
        :returns: response

        """
        return self._query('incidents', results_count, token=token, **elements)

    def update_incidents(self, order_id, incident_update_action, reasons):
        """Handle incidents created on orders

        Usage
        >>> response = manager.update_incidents(order_id, incident_update_action, reasons)

        :type order_id: str
        :param order_id: the unique FNAC identified for an order

        :type incident_update_action: str
        :param incident_update_action: the action to perform 
        ('refund' is the only available action for the moment) 

        :type reasons: dict
        :param reasons: 

        Example: 
        >>> reason = {"order_detail_id": 1, "refund_reason": 'no_stock'}
        >>> response = manager.update_incidents('07LWQ6278YJUI', 'refund', [reason])

        :rtype: Response
        :returns: response

        """
        incidents_update = create_xml_element(self.connection, self.token, 'incidents_update')
        order = etree.Element('order', order_id=order_id,
                              action=incident_update_action)

        for reason in reasons:
            order_detail = etree.Element("order_detail")
            etree.SubElement(order_detail, 'order_detail_id').text = str(reason['order_detail_id'])
            etree.SubElement(order_detail, 'refund_reason').text = str(reason['refund_reason'])
            order.append(order_detail)

        incidents_update.append(order)
        self.incidents_update_request = etree.tostring(incidents_update, **XML_OPTIONS)
        return self._get_response(incidents_update,
                self.incidents_update_request)

    def query_shop_invoices(self, results_count='100', token=None, **elements):
        """Return the download links to the shop's invoices

        Usage
        >>> response = manager.query_shop_invoices(results_count=results_count,
        token=token, **elements)

        :rtype: Response
        :returns: response

        """
        return self._query('shop_invoices', results_count, token=token, **elements)
