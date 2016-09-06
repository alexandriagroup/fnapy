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

URL        = "https://marketplace.ws.fd-recette.net/api.php/"
XHTML_NAMESPACE = "http://www.fnac.com/schemas/mp-dialog.xsd"
HEADERS = {'Content-Type': 'text/xml'}
XML_OPTIONS = {'pretty_print': True, 'xml_declaration': True, 'encoding': 'utf-8'}


# The elements for the requests
OFFERS_QUERY_ELEMENTS = (
    'paging', 'date', 'quantity', 'product_fnac_id', 'offer_fnac_id',
    'offer_seller_id'
)

ORDERS_QUERY_ELEMENTS = (
    'paging', 'date', 'sort_by', 'product_fnac_id', 'offer_fnac_id',
    'offer_seller_id', 'state', 'states', 'order_fnac_id', 'orders_fnac_id'
)

CLIENT_ORDER_COMMENTS_QUERY_ELEMENTS = (
    'paging', 'date', 'rate', 'client_order_comment_id', 'order_fnac_id'
)

MESSAGES_QUERY_ELEMENTS = (
    'paging', 'date', 'message_type', 'message_archived', 'message_state',
    'message_id', 'order_fnac_id', 'offer_fnac_id', 'offer_seller_id',
    'sort_by', 'message_from_types'
)

INCIDENTS_QUERY_ELEMENTS = (
    'paging', 'date', 'status', 'type', 'types', 'incident_id', 'incidents_id',
    'closed_statuses', 'closed_status', 'waiting_for_seller_answer',
    'opened_by', 'closed_by', 'sort_by', 'order', 'orders'
)

SHOP_INVOICES_QUERY_ELEMENTS = (
    'paging', 'date'
)

ORDER_ELEMENTS = (
    'shop_id', 'client_id', 'client_firstname', 'client_lastname',
    'client_email', 'adherent_number', 'order_id', 'order_culture', 'state',
    'created_at', 'fees', 'nb_messages', 'vat_rate', 'delivery_note',
    'shipping_address', 'billing_address', 'order_detail'
)

# The elements for the responses
OFFERS_UPDATE_RESPONSE_ELEMENTS = (
    'batch_id',
)

RESPONSE_ELEMENTS = {}
RESPONSE_ELEMENTS['offers_update'] = ('batch_id', )
RESPONSE_ELEMENTS['offers_query'] = (
    'page', 'total_paging', 'nb_total_per_page', 'nb_total_result', 'offer'
)
RESPONSE_ELEMENTS['orders_update'] = ('order', )
RESPONSE_ELEMENTS['orders_query'] = (
    'page', 'total_paging', 'nb_total_per_page', 'nb_total_result', 'order'
)
RESPONSE_ELEMENTS['batch_status'] = ('batch_id', 'offer')
RESPONSE_ELEMENTS['carriers_query'] = ('carrier',)
RESPONSE_ELEMENTS['incidents_query'] = (
    'page', 'total_paging',
    'nb_total_per_page', 'nb_total_result', 'incident'
)
RESPONSE_ELEMENTS['messages_query'] = (
    'page', 'total_paging',
    'nb_total_per_page', 'nb_total_result', 'message'
)
RESPONSE_ELEMENTS['messages_update'] = ('message',)
RESPONSE_ELEMENTS['pricing_query'] = ('pricing_product', )
RESPONSE_ELEMENTS['client_order_comments_query'] = ('comment',)
RESPONSE_ELEMENTS['client_order_comments_update'] = (
    'page', 'total_paging', 'nb_total_result', 'client_order_comment',
)
RESPONSE_ELEMENTS['shop_invoices_query'] = (
    'page', 'total_paging', 'nb_total_per_page', 'nb_total_result', 'shop_invoice',
)
