#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""

**fnapy** is a Python library using the FnacMarketPlace API to connect to your
own sales application to your FnacMarketplace seller account.  It uses the REST
WebService protocol to exchange data.

"""

# Python modules
from string import Template
import logging

# Third-party modules
import requests

# Project modules
from fnapy.utils import *
from fnapy.config import REQUEST_ELEMENTS, XHTML_NAMESPACE, HEADERS, XML_OPTIONS
from fnapy.compat import is_py3
from fnapy.connection import FnapyConnection
from fnapy.exceptions import FnapyPricingError


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def _create_docstring(query_type):
    """Create the docstring for a given query method"""
    _query_docstring = Template(FnapyManager._query.__doc__)
    service = query_type + '_query'
    param_fmt = ':param {param.name}: {param.desc}'.format
    parameters = "\n\t".join(param_fmt(param=param) for param in REQUEST_ELEMENTS[service])
    return _query_docstring.substitute(query_type=query_type,
                                       parameters=parameters)


class FnapyManager(object):
    """A class to manage the different services provided by the FNAC API"""

    VALID_QUERY_TYPES = ('offers', 'orders', 'client_order_comments',
                         'messages', 'incidents', 'shop_invoices')

    def __init__(self, connection):
        """Initialize the manager"""
        if not isinstance(connection, FnapyConnection):
            raise TypeError('You must provide a valid FnapyConnection instance.')

        self.connection = connection
        self.auth_request = None
        self.offers_query_request = None
        self.offers_update_request = None
        self.orders_query_request = None
        self.batch_query_request = None
        self.batch_status_request = None
        self.orders_update_request = None
        self.carriers_query_request = None
        self.client_order_comments_query_request = None
        self.client_order_comments_update_request = None
        self.messages_query_request = None
        self.messages_update_request = None
        self.incidents_query_request = None
        self.incidents_update_request = None
        self.pricing_query_request = None
        self.shop_invoices_query_request = None

        # The batch_id updated every time an offer is updated
        self.batch_id = None

        # the url of the entrypoint
        self.url = get_url(self.connection.sandbox)

        # Authenticate when the manager is instanciated
        self.authenticate()

    def _get_response(self, element, xml):
        """Send the request and return the response as a dictionary

        :type element: lxml.etree.Element
        :param element: the XML element
        
        :type xml: str
        :param xml: the XML string sent in the request

        :returns: :class:`Response <Response>` object
        """
        service = element.tag
        response = requests.post(self.url + service, xml, headers=HEADERS)
        response = Response(response.content)
        if response.dict.get(service + '_response', {}).get('error'):
            # Reauthenticate and update the element
            element.attrib['token'] = self.authenticate()
            setattr(self, service + '_request',
                    Request(etree.tostring(element, **XML_OPTIONS))) 
            # Resend the updated request
            response = requests.post(self.url + service,
                                     getattr(self, service + '_request').xml,
                                     headers=HEADERS)
            response = Response(response.content)
        return response

    def authenticate(self):
        """Authenticate to the FNAC API and return a token
        
        Usage::
        
            token = manager.authenticate()

        :returns: token
        :rtype: str
        
        """
        auth = etree.Element('auth', nsmap={None: XHTML_NAMESPACE})
        etree.SubElement(auth, 'partner_id').text = self.connection.partner_id
        etree.SubElement(auth, 'shop_id').text = self.connection.shop_id
        etree.SubElement(auth, 'key').text = self.connection.key
        self.auth_request = Request(etree.tostring(auth, **XML_OPTIONS))
        response = requests.post(self.url + 'auth', self.auth_request.xml,
                                 headers=HEADERS)
        self.token = parse_xml(response, 'token')
        return self.token

    def delete_offers(self, offer_references):
        """Delete the offers with the given offer_references (sku)

        Usage::

            response = manager.delete_offers(offer_references)

        :param offer_references: the list of SKUs corresponding to the offers
            you want to delete from your catalog

        :returns: :class:`Response <Response>` object

        """
        offers_update = create_xml_element(self.connection, self.token, 'offers_update')
        for offer_reference in offer_references:
            offer = etree.Element('offer')
            etree.SubElement(offer, "offer_reference",
                             type="SellerSku").text = etree.CDATA(offer_reference)
            etree.SubElement(offer, 'treatment').text = 'delete'
            offers_update.append(offer)

        self.offers_update_request = Request(etree.tostring(offers_update, **XML_OPTIONS))

        # the response contains the element batch_id
        response = self._get_response(offers_update, self.offers_update_request.xml)
        self.batch_id = response.dict['offers_update_response']['batch_id']
        return response

    # TODO Create a dictionary for the product_state
    def update_offers(self, offers_data):
        """Post the update offers and return the response

        Usage::

            response = manager.update_offers(offers_data)
        
        :type offers_data: list
        :param offers_data: the list of data to create the offers
                            where data is dictionary with the keys:

        * offer_reference  : the SKU (mandatory) 
        * product_reference: the EAN (optional)
        * price            : the price of the offer (optional)
        * product_state    : an integer representing the state of the product
                             (documentation needed) (optional)
        * quantity         : the quantity (optional)
        * description      : a description of the offer (optional)

        The exception FnapyUpdateOfferError is raised if:
        - offer_reference and at least one of the optional parameters (except
        product_reference) are not provided
        - offers_data is empty

        :returns: :class:`Response <Response>` object

        """
        offers_update = create_xml_element(self.connection, self.token, 'offers_update')

        if len(offers_data) == 0:
            msg = 'You must provide at least one offer_data.'
            raise FnapyUpdateOfferError(msg)

        for offer_data in offers_data:
            check_offer_data(offer_data)
            offer = create_offer_element(offer_data)
            offers_update.append(offer)
        self.offers_update_request = Request(etree.tostring(offers_update, **XML_OPTIONS))

        # the response contains the element batch_id
        response = self._get_response(offers_update, self.offers_update_request.xml)
        self.batch_id = response.dict['offers_update_response']['batch_id']
        return response

    # TODO Improve the documentation
    def update_orders(self, order_id, order_update_action, actions):
        """Update the selected order with an order_update_action

        Usage::

            response = manager.update_orders(order_id, order_update_action, actions)

        :type order_id: str
        :param order_id: Order unique identifier from FNAC

        :type order_update_action: str
        :param order_update_action: Group action type for order detail action

        :type actions: list
        :param actions: a list of dictionaries with 2 keys:
            `'order_detail_id'` and `'action'`

        :returns: :class:`Response <Response>` object

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

        Example: For this order (whose `order_id` is `'LDJEDEAS123'`), we have 2
        items. We decide to accept the first item and refuse the second::

            action1 = {"order_detail_id": 1, "action": "Accepted"}
            action2 = {"order_detail_id": 2, "action": "Refused"}
            response = manager.update_orders('LDJEDEAS123', 'accept_order', [action1, action2])

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
        self.orders_update_request = Request(etree.tostring(orders_update, **XML_OPTIONS))
        return self._get_response(orders_update, self.orders_update_request.xml)

    # FIXME The batch_status_response doesn't contain the attributes (status)
    def get_batch_status(self, batch_id=None):
        """Return the status for the given batch id

        Usage::

            response = manager.get_batch_status(batch_id=batch_id)

        ..note:: :class:`FnapyManager <FnapyManager>` stores the last `batch_id`
                 but you can provide a new one if needed.

        :param batch_id: the batch id (optional)
        :returns: :class:`Response <Response>` object

        """
        if batch_id is not None:
            self.batch_id = batch_id

        batch_status = create_xml_element(self.connection, self.token, 'batch_status')
        etree.SubElement(batch_status, 'batch_id').text = self.batch_id
        self.batch_status_request = Request(etree.tostring(batch_status, **XML_OPTIONS))
        return self._get_response(batch_status, self.batch_status_request.xml)

    # TODO Implement this method that should handle any arguments to create
    # the xml properly
    def _check_elements(self, valid_elements, selected_elements):
        for element in selected_elements:
            if element not in (x.name for x in valid_elements):
                raise ValueError('{} is not a valid element.'.format(element))

    def _query(self, query_type, results_count='', **elements):
        """Query your catalog and return the ${query_type} response

        Usage::

            response = manager.query_${query_type}(results_count=results_count,
                                            **elements)

        The available XML elements are the following parameters:

        ${parameters}

        :returns: :class:`Response <Response>` object

        Examples: 
        Find the 2 first items  of the catalog::

            response = manager.query_${query_type}(results_count=2, paging=1)

        Find the ${query_type} created between 2 dates::

            >>> from fnapy.utils import Query
            >>> date = Query('date', type='Modified')
                .between(min="2016-08-23T17:00:00+00:00",
                         max="2016-08-26T17:00:00+00:00")
            >>> response = manager.query_${query_type}(date=date)

        """
        if query_type in FnapyManager.VALID_QUERY_TYPES:
            query_type += "_query"
        else:
            raise ValueError("The query_type must be in {}".format(FnapyManager.VALID_QUERY_TYPES))

        # TODO Refactor: Use a dictionary to prevent code duplication
        # Check the queried elements
        self._check_elements(REQUEST_ELEMENTS[query_type], elements.keys())

        # Make sure we have unicode
        # paging = str(paging).decode('utf-8')
        results_count = str(results_count)#.decode('utf-8')

        # Create the XML element
        query = create_xml_element(self.connection, self.token, query_type)
        if results_count:
            query.attrib['results_count'] = results_count

        # Create the XML from the queried elements 
        if len(elements):
            for key, value in elements.items():
                # Handle cases where Query is used
                if isinstance(value, Query):
                    value = value.dict
                d = {key: value}
                queried_elements = etree.XML(dict2xml(d))
                query.append(queried_elements)

        setattr(self, query_type + '_request', Request(etree.tostring(query, **XML_OPTIONS)))
        query_xml = getattr(self, query_type + '_request').xml
        return self._get_response(query, query_xml)

    # TODO generator for the paging
    # TODO Allow to specify the type of date ('Created', 'Modified'...)
    def query_offers(self, results_count='', **elements):
        return self._query('offers', results_count, **elements)

    def query_orders(self, results_count='', **elements):
        return self._query('orders', results_count, **elements)

    def query_pricing(self, eans):
        """Retrieve the best prices applied to a given product within all Fnac
        marketplace sellers (Fnac included)

        Usage::

            response = manager.query_pricing(eans)

        :type eans: list or tuple
        :param eans: a list of EANs

        :returns: response

        .. note: If no price is found for a product, a :class:`FnapyPricingError <FnapyPricingError>`
            is raised.

        """
        pricing_query = create_xml_element(self.connection, self.token, 'pricing_query')

        for ean in eans:
            product_reference = etree.Element("product_reference", type="Ean")
            product_reference.text = str(ean)
            pricing_query.append(product_reference)

        self.pricing_query_request = Request(etree.tostring(pricing_query, **XML_OPTIONS))
        response = self._get_response(pricing_query, self.pricing_query_request.xml)

        # Check if any error is returned
        errors = response.element.xpath('//ns:error',
                namespaces={'ns': XHTML_NAMESPACE})
        if len(errors) > 0 and hasattr(errors[0], 'text'):
            for error in errors:
                product_reference = error.getprevious()
                logger.warning("EAN: {0}. {1}".format(product_reference.text,
                                                      error.text))
        return response

    def query_batch(self):
        """Return information about your currently processing import batches

        Usage::

            response = manager.query_batch()

        :returns: :class:`Response <Response>` object

        """
        batch_query = create_xml_element(self.connection, self.token, 'batch_query')
        self.batch_query_request = Request(etree.tostring(batch_query, **XML_OPTIONS))
        return self._get_response(batch_query, self.batch_query_request.xml)

    def query_carriers(self):
        """Return the available carriers managed on FNAC Marketplace platform
        
        Usage::

            response = manager.query_carriers()

        :returns: :class:`Response <Response>` object

        """
        carriers_query = create_xml_element(self.connection, self.token, 'carriers_query')
        etree.SubElement(carriers_query, "query").text = etree.CDATA("all")
        self.carriers_query_request = Request(etree.tostring(carriers_query, **XML_OPTIONS))
        return self._get_response(carriers_query, self.carriers_query_request.xml)

    def query_client_order_comments(self, results_count='', **elements):
        return self._query('client_order_comments', **elements)

    def update_client_order_comments(self, seller_comment, order_fnac_id):
        """Reply to client order comments

        Usage::

            response = manager.update_client_order_comments(seller_comment,
                                                            order_fnac_id)

        :type seller_comment: str
        :param seller_comment: The seller comment

        :type order_fnac_id: str
        :param order_fnac_id: Order unique identifier filter from FNAC

        :returns: :class:`Response <Response>` object

        """
        client_order_comments_update = create_xml_element(self.connection, self.token,
                                                          'client_order_comments_update')
        comment = etree.Element('comment', id=order_fnac_id)
        etree.SubElement(comment, 'comment_reply').text = etree.CDATA(seller_comment)
        client_order_comments_update.append(comment)
        self.client_order_comments_update_request = \
            Request(etree.tostring(client_order_comments_update, **XML_OPTIONS))
        return self._get_response(client_order_comments_update,
                self.client_order_comments_update_request.xml)

    def query_messages(self, results_count='', **elements):
        return self._query('messages', results_count, **elements)

    def update_messages(self, messages):
        """Update message sent on your offers or orders : reply, set as read, ...

        Usage::

            response = manager.update_messages(messages)

        :type messages: Message
        :param messages: the specified messages we want to update

        :returns: :class:`Response <Response>` object

        Example::

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

        self.messages_update_request = Request(etree.tostring(messages_update, **XML_OPTIONS))
        return self._get_response(messages_update, self.messages_update_request.xml)

    def query_incidents(self, results_count='', **elements):
        return self._query('incidents', results_count, **elements)

    def update_incidents(self, order_id, incident_update_action, reasons):
        """Handle incidents created on orders

        Usage::

            response = manager.update_incidents(order_id, 
                                                incident_update_action,
                                                reasons)

        :type order_id: str
        :param order_id: the unique FNAC identified for an order

        :type incident_update_action: str
        :param incident_update_action: the action to perform (`'refund'` is the
                                       only available action for the moment) 

        :type reasons: list
        :param reasons: the reasons of the incident for this order

        Example::

            reason = {"order_detail_id": 1, "refund_reason": 'no_stock'}
            response = manager.update_incidents('07LWQ6278YJUI', 'refund', [reason])

        :returns: :class:`Response <Response>` object

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
        self.incidents_update_request = \
            Request(etree.tostring(incidents_update, **XML_OPTIONS))
        return self._get_response(incidents_update,
                self.incidents_update_request.xml)

    def query_shop_invoices(self, results_count='', **elements):
        return self._query('shop_invoices', results_count, **elements)


# Dynamically set the docstrings for some query methods
for query_type in FnapyManager.VALID_QUERY_TYPES:
    method = getattr(FnapyManager, 'query_' + query_type)
    if is_py3:
        method.__doc__ = _create_docstring(query_type)
    else:
        method.__func__.__doc__ = _create_docstring(query_type)

