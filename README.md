# Description

A client to connect to the FNAC Marketplace


# Usage

* Create a connection to the FNAC API

```python
conn = FnapyConnection(pattern_id, shop_id, key)
```

* Create the manager for the FNAC API

```python
manager = FnapyManager(conn)
```

Now you should be able to access the different web services

* Update the offers

```python
offer_data1 = {'product_reference':'0711719247159',
        'offer_reference':'B76A-CD5-153',
        'price':15, 'product_state':11, 'quantity':10, 
        'description': 'New product - 2-3 days shipping, from France'}
offer_data2 = {'product_reference':'5030917077418',
        'offer_reference':'B067-F0D-75E',
        'price':20, 'product_state':11, 'quantity':16, 
        'description': 'New product - 2-3 days shipping, from France'}

offers_data = [offers_data1, offer_data2]
response = manager.update_offers(offers_data)
```

The `offers_update` service returns the `batch_id` which will be useful to know the
status of this operation. 

* Get the batch status

```python
batch_id = response.['offers_update_response']['batch_id']
batch_status = manager.get_batch_status(batch_id)
```

* Query the offers

When you're satisfised with your offers you may want to know if they were
actually created and retrieve information about them.

Let's say you want to know the offers created between 2016-08-25 and 2016-08-31:

```python
dmin = datetime(2016, 8, 25, 0, 0, 0).replace(tzinfo=pytz.utc)
dmax = datetime(2016, 8, 31, 0, 0, 0).replace(tzinfo=pytz.utc)
date = {'@type': 'Created',
        'min': {'#text': dmin.isoformat()},
        'max': {'#text': dmax.isoformat()}
        }
response = manager.query_offers(date=date)
```

* Query your orders

Once customers placed an order on your items in your catalog, you can query
these orders.

Let's suppose you want to retrieve the first 10 created orders:

```python
response = manager.query_orders(results_count=10, paging=1)
```

