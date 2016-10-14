.. _quickstart:

Quickstart
==========

This page gives a good introduction in how to get started with fnapy.

Before starting, make sure you have your credentials to connect to the FNAC
API.


* Create a connection to the FNAC Marketplace API with your credentials::

    >>> from fnapy.fnapy_manager import FnapyManager
    >>> connection = FnapyConnection(credentials)

* Create the manager::

    >>> from fnapy.connection import FnapyConnection
    >>> manager = FnapyManager(connection)

Now you should be able to access the different web services.


Update your offers
------------------

Let's create some offers in our catalog::

    offer_data1 = {'product_reference':'0711719247159',
            'offer_reference':'B76A-CD5-153',
            'price':15, 'product_state':11, 'quantity':10, 
            'description': 'New product - 2-3 days shipping, from France'}
    offer_data2 = {'product_reference':'5030917077418',
            'offer_reference':'B067-F0D-75E',
            'price':20, 'product_state':11, 'quantity':16, 
            'description': 'New product - 2-3 days shipping, from France'}

    response = manager.update_offers([offers_data1, offer_data2])

Behind the scene, the manager sent an XML request to the `offers_update`
service. We can have a look at this request with the attribute `offers_update_request`::

    >>> request = manager.offers_update_request
    >>> print request.xml
    <?xml version='1.0' encoding='utf-8'?>
    <offers_update xmlns="http://www.fnac.com/schemas/mp-dialog.xsd" partner_id="XXX" shop_id="XXX" token="XXX">
      <offer>
        <product_reference type="Ean">0711719247159</product_reference>
        <offer_reference type="SellerSku"><![CDATA[B76A-CD5-153]]></offer_reference>
        <price>15</price>
        <product_state>11</product_state>
        <quantity>10</quantity>
        <description><![CDATA[New product - 2-3 days shipping, from France]]></description>
      </offer>
      <offer>
        <product_reference type="Ean">5030917077418</product_reference>
        <offer_reference type="SellerSku"><![CDATA[B067-F0D-75E]]></offer_reference>
        <price>20</price>
        <product_state>11</product_state>
        <quantity>16</quantity>
        <description><![CDATA[New product - 2-3 days shipping, from France]]></description>
      </offer>
    </offers_update>

Actually this request is an instance of the :class:`Request <Request>` class.
We'll talk about it later. For now, let's see what we've got in our response::

    >>> print response.xml
    <?xml version="1.0" encoding="utf-8"?>
    <offers_update_response status="OK" xmlns="http://www.fnac.com/schemas/mp-dialog.xsd">
        <batch_id>88BD9517-A73C-78E0-04DB-AC5ADE1D63F6</batch_id>                  
    </offers_update_response>

The response sent by the server is just an instance of the :class:`Response
<Response>` class. We can see that the status of the response is OK and the
batch_id is 88BD9517-A73C-78E0-04DB-AC5ADE1D63F6. This is basically the id
you'll have to use to get information about the status of your offers.


Get the batch status
--------------------

::

    batch_id = response.dict['offers_update_response']['batch_id']
    response = manager.get_batch_status(batch_id)

Note that :class:`FnapyManager <FnapyManager>` stores the last `batch_id` so if
you want the latest `batch_status` you can do::

    response = manager.get_batch_status()


Query the offers
----------------

When you're satisfised with your offers you may want to know if they were
actually created and retrieve information about them.

Let's say you want to know the offers created between 2016-08-25 and 2016-08-31::

    from fnapy.utils import Query
    dmin = datetime(2016, 8, 25, 0, 0, 0).replace(tzinfo=pytz.utc).isoformat()
    dmax = datetime(2016, 8, 31, 0, 0, 0).replace(tzinfo=pytz.utc).isoformat()
    date Query('date', type='Created').between(min=dmin, max=dmax)
    response = manager.query_offers(date=date)


Query the pricing
-----------------

In order to stay competitive, you have to know the offers created by the
other sellers for a list of EANs or at least the current best offer these
products. You can get these information with `query_pricing`::

    response = manager.query_pricing(eans=eans)


Delete offers
-------------

You can delete the offers you created with `delete_offers`::

    response = manager.delete_offers(offer_references)

where `offer_references` is a list of SKUs.


Query the orders
----------------

Once customers placed an order on your items in your catalog, you can query
these orders.

If you want to retrieve the first 10 created orders, you'll have to sent this
request with::

    response = manager.query_orders(results_count=10, paging=1)


Update the orders
-----------------

Orders statuses are following this workflow:

Created > Accepted > ToShip > Shipped > Received

The seller acts only at acceptation and shipping steps.

This is the how we accept the first and refuse the second order for the
order_id 003ECCA1YVFBW::

    action1 = {"order_detail_id": 1, "action": "Accepted"}
    action2 = {"order_detail_id": 2, "action": "Refused"}
    actions = [action1, action2]
    response = manager.update_orders('003ECCA1YVFBW', "accept_order", actions)

.. todo:: Add example for "accept_all_orders"

.. todo:: Add the section using query_orders to check the order was created
          successfully

Request and Response
--------------------

Both :class:`Request <Request>` and :class:`Response <Response>` share the same
interface.



