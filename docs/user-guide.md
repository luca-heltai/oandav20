# User guide

## Introduction

Oandav20 is designed to be rather SDK than ordinary REST API wrapper which may explicitly cover every possible endpoints and maybe you never use it at all.

Unlike the wrappers this package extends the default Oanda API by more useful methods which in fact combine several endpoints at once.

For example:

- update a pending order without closing one and creating new one
- bulk cancel all pendings orders or filtered (eg. only the fx pairs which contain "USD")
- bulk close all open trades or filtered

There is also time-saving feature:

- remember trading account ID and reuse it in methods where required (useful, if you manage only 1 trading account)

## Installation

If you haven't installed it yet and have Python 3.5.x version and above, then do:

```
pip install oandav20
```

## Quickstart

### Oanda object

The main object for interaction with the Oanda API server is `Oanda` class:

```python
>>> from oandav20 import Oanda
>>>
>>> o = Oanda("environment", "access_token", "default_id")
```

As you may see, `Oanda` requires 3 arguments:

1. environment = "DEMO" or "REAL"
2. access_token = your generated access token which will be used for authentication (navigate to you Oanda account dashboard and click to `Manage API Access`)
3. default_id = your default trading accout ID (in the dashboard click to `Manage Funds`)

Before we start calling methods on the `o` object, I would like to tell you what is really happening in background.

By initialization the `o` object is is prepared one persistent TCP/IP connection with the Oanda server. Every time you will call a method, an HTTP request is send and waiting for response.

Be aware that maximum allowed number of requests is 30 per second. Any extra requests will be ignored.

When it comes to finishing trading, it would be very pleasant if you explicitly close the persistent HTTP connection (session):

```python
>>> o.client.close()
```

### Account methods

#### Getting account details

To get account summary details for the default trading account just call:

```python
>>> o.get_account_summary()
>>>
>>> # For different trading account:
>>> o.get_account_summary("another_trading_account_ID")  # or
>>> o.get_account_summary(account_id="another_id")
```

The output would be in poorly arranged dictionary (alias JSON object), so I will use `json` standard module for nice priting.

```python
>>> import json
>>>
>>> print(json.dumps(o.get_account_summary(), indent=4, sort_keys=True))
... {
...     "account": {
...         "NAV": "43650.78835",
...         "alias": "My New Account #2",
...         "balance": "43650.78835",
...         "createdByUserID": <USERID>,
...         "createdTime": "2015-08-12T18:21:00.697504698Z",
...         "currency": "CHF",
...         "hedgingEnabled": false,
...         "id": "<ACCOUNT>",
...         "lastTransactionID": "6356",
...         "marginAvailable": "43650.78835",
...         "marginCloseoutMarginUsed": "0.00000",
...         "marginCloseoutNAV": "43650.78835",
...         "marginCloseoutPercent": "0.00000",
...         "marginCloseoutPositionValue": "0.00000",
...         "marginCloseoutUnrealizedPL": "0.00000",
...         "marginRate": "0.02",
...         "marginUsed": "0.00000",
...         "openPositionCount": 0,
...         "openTradeCount": 0,
...         "pendingOrderCount": 0,
...         "pl": "-56034.41199",
...         "positionValue": "0.00000",
...         "resettablePL": "-56034.41199",
...         "unrealizedPL": "0.00000",
...         "withdrawalLimit": "43650.78835"
...     },
...     "lastTransactionID": "6356"
... }
```

I expect that you know what the keys mean. If not, use official definitions explanation by Oanda [HERE](http://developer.oanda.com/rest-live-v20/account-df/). In the menu at the bottom are also covered definitions for other methods I will be using.

**Note**: the `account_id` argument works almost for every method. If you pass an invalid ID, HTTPError from the `requests` library will be raised:

```python
>>> o.get_account_summary("foo")
Traceback ...
...
requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: ...
```

There is also very similar but verbose variant of this method and it's:

```python
>>> print(json.dumps(o.get_account(), indent=4, sort_keys=True))
... {
...     "account": {
...         ...
...         "orders": [
...             # list of pending orders
...         ],
...         "positions": [
...             # list of positions (finished trades)
...         ],
...         "trades": [
...             # list of open trades
...         ]
...         ...
...     }
... }
```

Dictionary keys for the "orders", "positions" and "trades" will be covered lately.

### Pricing methods

#### Actual price

To get actual pricing information for one or more instruments:

```python
>>> print(json.dumps(o.get_pricing(["EUR_USD"]), indent=4, sort_keys=True))
>>> {
...     "prices": [
...         {
...             "asks": [
...                 {
...                     "liquidity": 10000000,
...                     "price": "1.13028"
...                 },
...                 {
...                     ...
...                 }
...             ],
...             "bids": [
...                 {
...                     "liquidity": 10000000,
...                     "price": "1.13015"
...                 },
...                 {
...                     ...
...                 }
...             ],
...             "closeoutAsk": "1.13032",
...             "closeoutBid": "1.13011",
...             "instrument": "EUR_USD",
...             "quoteHomeConversionFactors": {
...                 "negativeUnits": "0.95904000",
...                 "positiveUnits": "0.95886000"
...             },
...             "status": "tradeable",
...             "time": "2016-06-22T18:41:36.201836422Z",
...             "unitsAvailable": {
...                 "default": {
...                     "long": "2013434",
...                     "short": "2014044"
...                 },
...                 "openOnly": {
...                     "long": "2013434",
...                     "short": "2014044"
...                 },
...                 "reduceFirst": {
...                     "long": "2013434",
...                     "short": "2014044"
...                 },
...                 "reduceOnly": {
...                     "long": "0",
...                     "short": "0"
...                 }
...             }
...         }
...     ]
... }
```

**Note**: This is temporary solution before Oanda implement streaming endpoint. So you have to implement an infinite loop to call over and over the `.get_pricing` method and check if it's time to trade or not.

Example:

```python
...

while True:
    variable = o.get_pricing(["your_instruments"])

    if <your_condition>:
        call_some_function()

    # maybe time sleep

...
```

Keys "asks" and "bids" may have 2 or more dictionary inside. From my observation is fine to work only with the first one to get ask and bid price:

```python
>>> price = o.get_pricing(["EUR_USD"])
>>> ask_price = price["prices"][0]["asks"][0]["price"]  # 1.13028
>>> bid_price = price["prices"][0]["bids"][0]["price"]  # 1.13015
```

List of all instruments codes is available [HERE](https://github.com/nait-aul/oandav20/blob/master/oandav20/mixins/account.py).

If you pass more instruments codes at once, the pricing information for them will be ordered in the same order as you passed the codes:

```python
>>> price = o.get_pricing(["AUD_USD", "EUR_USD", "GBP_USD"])
>>> price["prices"][2]["instrument"] == "GBP_USD"
True
```

