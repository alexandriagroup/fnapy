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
