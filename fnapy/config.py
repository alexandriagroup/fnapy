#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Useful constants and configs.
"""

XHTML_NAMESPACE = "http://www.fnac.com/schemas/mp-dialog.xsd"
HEADERS = {'Content-Type': 'text/xml'}
XML_OPTIONS = {'pretty_print': True, 'xml_declaration': True, 'encoding': 'utf-8'}


# The sub elements in the order element
ORDER_ELEMENTS = (
    'shop_id', 'client_id', 'client_firstname', 'client_lastname',
    'client_email', 'adherent_number', 'order_id', 'order_culture', 'state',
    'created_at', 'fees', 'nb_messages', 'vat_rate', 'delivery_note',
    'shipping_address', 'billing_address', 'order_detail'
)

class Parameter(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def change_desc(self, new_desc):
        """Return a new parameter object with a new description

        :param new_desc: a new description

        Sometimes in the FNAC API, the name of a node is used with a different
        type and a different meaning. This method allows to deal with these
        inconsistencies. As we don't manage the types, we just need to change
        the description.

        """
        return Parameter(self.name, new_desc)
        


paging               = Parameter('paging', 'Page number to fetch')
date                 = Parameter('date', 'Date filter')
quantity             = Parameter('quantity', 'Quantity filter')
product_fnac_id      = Parameter('product_fnac_id', "Product's unique identifier from fnac")
offer_fnac_id        = Parameter('offer_fnac_id', 'Offer unique identifier from fnac')
offer_seller_id      = Parameter('offer_seller_id', 'Offer unique identifier from seller (SKU)')
sort_by              = Parameter('sort_by', 'Quantity filter')
state                = Parameter('state', 'Order state filter')
states               = Parameter('states', 'Multiple order state filter')
order_fnac_id        = Parameter('order_fnac_id', 'Order unique identifier filter')
orders_fnac_id       = Parameter('orders_fnac_id', 'Multiple order unique identifier filter')
rate                 = Parameter('rate', 'Order rate filter')
message              = Parameter('message', 'Messages to update')
message_type         = Parameter('message_type', 'Message type filter')
message_archived     = Parameter('message_archived', 'Message is archived or not filter')
message_state        = Parameter('message_state', 'Message state')
message_id           = Parameter('message_id', 'Message unique identifier from fnac filter')
message_from_types   = Parameter('message_from_types', 'Messages author filter')
status               = Parameter('status', 'Status of the incident')
type                 = Parameter('type', 'Incident order detail opening reason')
types                = Parameter('types', 'Define the opening reasons of the incidents to be retrieved.')
incident_id          = Parameter('incident_id', 'A unique incident id')
incidents_id         = Parameter('incidents_id', 'Can contain multiple incident_id node (up to 50 max)')
closed_statuses      = Parameter('closed_statuses', 'Can contain multiple closed_status node (up to 50 max)')
closed_status        = Parameter('closed_status', 'Incident closing reason')
opened_by            = Parameter('opened_by', 'Who opened the incident')
closed_by            = Parameter('closed_by', 'Who closed the incident')
order                = Parameter('order', 'Orders to update')
orders               = Parameter('orders', 'Can contains multiple order node (up to 50 max)')
page                 = Parameter('page', 'Page number')
total_paging         = Parameter('total_paging', 'Number of pages available')
nb_total_per_page    = Parameter('nb_total_per_page', 'Number of results per page')
nb_total_result      = Parameter('nb_total_result', 'Number of results')
batch_id             = Parameter('batch_id', 'Batch unique identifier from fnac')
offer                = Parameter('offer', 'Offers')
batch                = Parameter('batch', 'List of batches')
nb_batch_running     = Parameter('nb_batch_running', 'Number of batches being processed')
nb_batch_active      = Parameter('nb_batch_active', 'Number of batches waiting to be processed')
carrier              = Parameter('carrier', 'A carrier')
incident             = Parameter('incident', 'Incident information')
pricing_product      = Parameter('pricing_product', 'Pricings of product')
comment              = Parameter('comment', 'Updated comments')
shop_invoice         = Parameter('shop_invoice', 'Shop invoices')
waiting_for_seller_answer = Parameter('waiting_for_seller_answer',
                                      """Fnac customer service can ask the seller
                                      to deal specifically with an incident.""")
client_order_comment = Parameter('client_order_comment', 'Client order comments')
client_order_comment_id = Parameter('client_order_comment_id',
                                    'Order unique identifier filter from fnac')

product_reference = Parameter('product_reference', 'Product referenc')
offer_reference = Parameter('offer_reference', 'Offer reference')
price = Parameter('price', 'Offer price')
product_state = Parameter('product_state', 'Product state of offer')
description = Parameter('description', 'Product description')
internal_comment = Parameter('internal_comment',
                             'Offer internal comment for personal use')
showcase = Parameter('showcase', 'Offer position in shop’s showcase')
treatment = Parameter('treatment', 'Treatment to do on offer')
pictures = Parameter('pictures', 'Add pictures to offer')

# The elements for the requests
REQUEST_ELEMENTS = {}
REQUEST_ELEMENTS['offers_query'] = (
    paging, date, quantity, product_fnac_id, offer_fnac_id,
    offer_seller_id
)
REQUEST_ELEMENTS['offers_update'] = (
    product_reference, offer_reference, price, product_state,
    quantity.change_desc('Offer quantity'), description,
    internal_comment, showcase, treatment, pictures
)
REQUEST_ELEMENTS['orders_query'] = (
    paging, date, sort_by, product_fnac_id, offer_fnac_id,
    offer_seller_id, state, states, order_fnac_id, orders_fnac_id
)
REQUEST_ELEMENTS['client_order_comments_query'] = (
    paging, date, rate, client_order_comment_id, order_fnac_id
)
REQUEST_ELEMENTS['messages_query'] = (
    paging, date, message_type, message_archived, message_state,
    message_id, order_fnac_id, offer_fnac_id, offer_seller_id,
    sort_by, message_from_types
)
REQUEST_ELEMENTS['incidents_query'] = (
    paging, date, status, type, types, incident_id, incidents_id,
    closed_statuses, closed_status, waiting_for_seller_answer,
    opened_by, closed_by, sort_by,
    order.change_desc('A unique order id'), 
    orders.change_desc('Can contains multiple order node (up to 50 max)')
)
REQUEST_ELEMENTS['shop_invoices_query'] = (
    paging, date
)

# The elements for the responses
RESPONSE_ELEMENTS = {}
RESPONSE_ELEMENTS['offers_update'] = (
    batch_id, 
)
RESPONSE_ELEMENTS['offers_query'] = (
    page, total_paging, nb_total_per_page, nb_total_result, offer
)
RESPONSE_ELEMENTS['orders_update'] = (
    order, 
)
RESPONSE_ELEMENTS['orders_query'] = (
    page, total_paging, nb_total_per_page, nb_total_result,
    order.change_desc('Orders')
)
RESPONSE_ELEMENTS['batch_status'] = (batch_id, offer)
RESPONSE_ELEMENTS['batch_query'] = (
    batch, nb_batch_running, nb_batch_active
)
RESPONSE_ELEMENTS['carriers_query'] = (carrier,)
RESPONSE_ELEMENTS['incidents_query'] = (
    page, total_paging,
    nb_total_per_page, nb_total_result, incident
)
RESPONSE_ELEMENTS['incidents_update'] = (
    order.change_desc('Seller Order in fnac marketplace'),
)
RESPONSE_ELEMENTS['messages_query'] = (
    page, total_paging,
    nb_total_per_page, nb_total_result,
    message.change_desc('Messages list')
)
RESPONSE_ELEMENTS['messages_update'] = (message,)
RESPONSE_ELEMENTS['pricing_query'] = (pricing_product, )
RESPONSE_ELEMENTS['client_order_comments_query'] = (
    page, total_paging, nb_total_per_page, nb_total_result, client_order_comment,
)
RESPONSE_ELEMENTS['client_order_comments_update'] = (comment,)
RESPONSE_ELEMENTS['shop_invoices_query'] = (
    page, total_paging, nb_total_per_page, nb_total_result, shop_invoice,
)
