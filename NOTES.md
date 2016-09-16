# Notes


## Process

You start creating offers in your catalog with the `update_offers` service.
The returned response contains a `batch_id` that allows you to check
the status of your offers.

When you finished updating your offers, you can check if they were actually
created with the `offers_query` service.

Now that you have offers in your catalog, you can retrieve the orders with the
`orders_query` service. 

In order to update the orders (accept, refuse or ship it) you have to use the
`orders_update` service with the `order_id` and the selected action.


### Offers update

* Description 

This service is used to manage your catalog. It allows you to add, update or delete offers.

* Process

1. A valid authentification token is needed.
2. The partner sends a list of offers to add, update or delete.
3. The service returns a batch identifier. With that id you can retrieve the
   process report of the sent feed by using _Batch Status_

* Limitation 

The recommended number of offers to update at once is 10 000. The service
doesn't provide a "purge and replace" mode. To delete offers, you have to use
the <treatment> element on each offer to remove.


### Creation of an offer

We need 5 mandatory parameters:

* a product reference (such as EAN)
* a seller offer reference (such as SKU)
* a product state
* a price
* a quantity

and 3 optional parameters:

* a description of the product
* a showcase number (the position of the offer in the showcase)
* an internal comment visible only by yourself in the seller account


### batch_status

The status of the request is accessed with a batch id. You can use this id to
know the processing status of the request.

* Description 

Presents the status of the last operation. More details are available in the
sub levels presenting errors

The status has 3 main states:

- ACTIVE: the batch is queued and ready to be processed
– RUNNING: Process is still running
– OK: Process finished without any error or warning

If something went wrong and the final status is not 'OK', the state will be:

– WARNING: Process finished with at least a warning and no error
– ERROR: Process finished with at least an error, but no blocking error was encountered
– FATAL: A fatal error occured while processing, the process was not
  done completely or even completely aborted



### offers_query

* Description

This is service is used to retrieve offers from your shop catalog according to
submitted criteria.

* Process

1. A valid authentification token is needed.
2. The partner calls the service with criteria.
3. The service returns the selected offers.

* Limitation

Query is limited to 10 000 offers per call. Above this limit, an error will be
thrown in the response.


### orders_query

### orders_update

* Description

This is service is used to update the status of your orders (accepting,
shipping or updating shipping information).

* Process

1. A valid authentification token is needed.
2. The partners calls the service by sending list of orders and the action to
   make on the related order details (accept, refuse, etc.).
3. The service returns a report of the update processing.

* Limitation

You can update up to 25 orders at once.


Orders statuses follow this workflow:

1. Created
2. Accepted
3. ToShip
4. Shipped
5. Received


### order_update_action

* Description

Defines the actions available on an order from the seller's side

* Restriction

Enumerate:
    - accept_order: The action for the order is accepting orders by the seller
    - confirm_to_send: The action for the order is confirming sending orders by the seller
    - update: The action for the order is updating orders by the seller
    - accept_all_orders: The action for the order is accepting or refusing all order_details of the order by the seller
    - confirm_all_to_send: The action for the order is confirming sending all order_details by the seller
    - update_all: The action for the order is to update tracking information for all order_details


### pricing_query

* Description

Compare price between all marketplace shop and fnac for a specific product.

* Process

    A valid authentification token is needed.
    The partner calls service with a list of product reference
    The service returns for each product reference a list of the lowest prices
    suggested by FNAC Marketplace sellers.

The number of product references to request is limited to 10.


## How we test fnapy

We do 2 kinds of test: online and offline tests.

### Online tests

They allow us to make sure a given XML request gives us the response
containting the information we need. 

Here is the procedure we use for these tests:

- we create the XML request in a file called <action>_request.xml, 
- read it
- send this XML with `requests`.
- we test the content the of the response
- store the response in a XML file called <action>_response.xml


### Offline tests

They allow us to make sure our library will always send the request that will
produce the response we expect. In particular, these tests will be used as
regression tests as we refactor the code.

Testing our library in the online tests would be a hassle as some responses can
take a long time. In order to avoid depending on the speed of the server, we
mock it by monkey-patching `requests` so that the response returned is the the
one we previously saved in the online tests (<action>_response.xml). As we know
this response is correct, we just need to test that the XML request sent by our
library corresponds to the XML request we used in the online tests
(<action>_request.xml)

Here is the corresponding procedure:

- we monkey-patch `requests`,
- run the function of our library generating the request we want
- then we test the request generated has the same information as <action>_request.xml


## Product states

Here is an example of what we are supposed to get with the
`pricing_query_response`:

```xml
    <pricing_query_response xmlns="http://www.fnac.com/schemas/mp-dialog.xsd" status="OK">
        <pricing_product>
            <product_reference type="Ean">0886971942323</product_reference>
            <ean>0886971942323</ean>
            <product_url><![CDATA[http://www4.rec1.fnac.dev/Shelf/Article4.aspx?prid=2066124]]></product_url>
            <seller_price>14</seller_price>
            <seller_shipping>2.39</seller_shipping>
            <seller_offer_sku>4F1A-28E-8BE</seller_offer_sku>
            <seller_offer_state>2</seller_offer_state>
            <seller_adherent_price>10</seller_adherent_price>
            <seller_adherent_shipping>2.39</seller_adherent_shipping>
            <seller_adherent_offer_state>2</seller_adherent_offer_state>
            <seller_adherent_offer_sku>4F1A-28E-8BE</seller_adherent_offer_sku>
            <new_price>0.90</new_price>
            <new_shipping>2.39</new_shipping>
            <refurbished_price/>
            <refurbished_shipping/>
            <used_price>2.90</used_price>
            <used_shipping>2.39</used_shipping>
            <new_adherent_price/>
            <new_adherent_shipping/>
            <refurbished_adherent_price/>
            <refurbished_adherent_shipping/>
            <used_adherent_price>1.50</used_adherent_price>
            <used_adherent_shipping>2.39</used_adherent_shipping>
        </pricing_product>
    </pricing_query_response>
```

The tags starting with `seller_` designate the seller's offer. The product
state of the seller is given by `<seller_offer_state>`. Its value is 2 which means 
"used product in very good state". There's a total of 11 product states:

* 1: This product is a **used** product like as new
* 2: This product is a **used** product in very good state
* 3: This product is a **used** in good state
* 4: This product is a **used** product in correct state
* 5: This product is a collection product like as **new**
* 6: This product is a collection product in very **good** state
* 7: This product is a collection product in **good** state
* 8: This product is a collection product in *correct* state
* 10: This product is a **refurbished** product
* 11: This product is a **new** product

However only information about the product state we have from this response is
the summed up within 3 generic states: **new**, **refurbished** and **used** 
(cf the corresponding nodes).
This means we lose some information when we query the pricing.
