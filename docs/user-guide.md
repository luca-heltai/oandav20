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
$ pip install oandav20
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

1. `environment` = "DEMO" or "REAL"
2. `access_token` = your generated access token which will be used for authentication (navigate to you Oanda account dashboard and click to `Manage API Access`)
3. `default_id` = your default trading accout ID (in the dashboard click to `Manage Funds`)

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

The output would be in poorly arranged dictionary (alias JSON object), so I use `json` standard module for nice priting here and for every method below returning JSON.


```python
>>> o.get_account_summary()
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
>>> o.get_account()
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

Dictionary keys for the `orders`, `positions` and `trades` will be covered lately.

### Pricing methods

#### Getting actual pricing

To get actual pricing information for one or more instruments:

```python
>>> o.get_pricing(["EUR_USD"])
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

Keys `asks` and `bids` may have 2 or more dictionary inside. From my observation is fine to work only with the first one to get ask and bid price:

```python
>>> price = o.get_pricing(["EUR_USD"])
>>> ask_price = price["prices"][0]["asks"][0]["price"]  # 1.13028
>>> bid_price = price["prices"][0]["bids"][0]["price"]  # 1.13015
```

List of all instruments codes is available [HERE](https://github.com/nait-aul/oandav20/blob/master/oandav20/mixins/account.py). Keys represent human values and values instrument codes. If you pass invalid instrument code, `ValueError` will be raised.

If you pass more instruments codes at once, the pricing information for them will be ordered in the same order as you passed the codes:

```python
>>> price = o.get_pricing(["AUD_USD", "EUR_USD", "GBP_USD"])
>>> price["prices"][2]["instrument"] == "GBP_USD"
True
```

### Orders methods

#### Creating orders

To create an order with minimum arguments:

```python
>>> o.create_order("MARKET", "EUR_USD", "SELL", 1000)
12345
```

**Note**: Oanda allows to trade even with 1 single unit.

Recapitulation of units size:

| common term | size |
| --- | --- |
| 1 micro lot | 1000|
| 1 mini lot | 10000 |
| 1 lot | 100000 |

The returned value is Oanda order ID which we may use in other methods such as getting order details or closing orders.

Now I would like to introduce you nice Oanda feature and it's using own ID / tags / comments:

```python
>>> o.create_order("LIMIT", "EUR_USD", "BUY", 1000, price=0.5,
...                own_id="EUR_USD_1", tag="trading system A",
...                comment="support level")
True
```

The `EUR_USD_1` ID will same for orders and trades manipulating which is much more better then work with Oanda IDs (one for orders, another different for trades).

I bet you want also use stoploss and takeprofit right? Let's do it:

```python
>>> o.create_order("STOP", "EUR_USD", "SELL", 1000, 1.5, own_id="EUR_USD_2",
...                stoploss=1.51, takeprofit=1.49)
True
```

**Note**: Trailing stoploss is not implemented due to failed tests. If you want this feature, let me know.

Finally, you may also use short version (aliases):

```python
>>> o.create_market_order("EUR_USD", "...")
>>> o.create_limit_order("EUR_USD", "...")
>>> o.create_stop_order("EUR_USD", "...")
```

**Note**: Order type `MARKET IF TOUCHED` is also not implemented (I consider it useless).

#### Checking order details

To control your order details or check order status:

```python
>>> o.get_order(own_id="EUR_USD_3")  # or Oanda order ID o.get_order(123)
... {
...     "lastTransactionID": "6375",
...     "order": {
...         "clientExtensions": {
...             "comment": "New idea for trading",
...             "id": "EUR_USD_3",
...             "tag": "strategy_9"
...         },
...         "createTime": "2016-06-22T18:41:29.294265338Z",
...         "id": "6375",
...         "instrument": "EUR_USD",
...         "partialFill": "DEFAULT_FILL",
...         "positionFill": "POSITION_DEFAULT",
...         "price": "1.30000",
...         "state": "PENDING",
...         "timeInForce": "GTC",
...         "triggerCondition": "TRIGGER_DEFAULT",
...         "type": "STOP",
...         "units": "10000"
...     }
... }
```
The order above is still PENDING. Once it will be filled, the `state` key will show value `FILLED` and from the order becomes a trade.

#### Updating pending orders

Suppose I sent an sell stop order with bad values and hopefully it's still pending, so I want to update / repair it:

```python
>>> o.update_order(own_id="EUR_USD_4", price=1.0020, price_bound=1.0018,
...                stoploss=1.0040, takeprofit=1.0)
True
```

Notice the `price_bound` argument. It's next super feature from Oanda which works only for market and stop orders. Price bound means the worst filled price you accept.

If you send an market order with price level X and price bound Y and market conditions quickly changed at that time that actual price is over price bound Y, the order won't be filled. 

#### Canceling pending orders

I guess you except something like `.close_order()`, do you? If so, you've got it :+1:.

```python
>>> o.close_order(own_id="EUR_USD_5")
True
```

**Note**: Other order methods are described in the [API reference][api-reference].

### Trades methods

#### Checking trade details

In order to get trade details must be first filled an order. If this condition is met, then do:

```python
>>> o.get_trade(own_id="EUR_USD_6")
... {
...     "lastTransactionID": "1025",
...     "trade": {
...         "clientExtensions": {
...             "id": "EUR_USD_6",
...         },
...         "currentUnits": "1",
...         "financing": "0.0000",
...         "id": "1023",
...         "initialUnits": "1",
...         "instrument": "EUR_USD",
...         "openTime": "2016-08-17T15:21:29.306846600Z",
...         "price": "1.12860",
...         "realizedPL": "0.0000",
...         "state": "OPEN",
...         "stopLossOrder": {
...             "createTime": "2016-08-17T15:21:29.715039917Z",
...             "id": "1025",
...             "price": "1.12507",
...             "state": "PENDING",
...             "timeInForce": "GTC",
...             "tradeID": "1023",
...             "triggerCondition": "TRIGGER_DEFAULT",
...             "type": "STOP_LOSS"
...         },
...         "takeProfitOrder": {
...             "createTime": "2016-08-17T15:21:29.715039917Z",
...             "id": "1024",
...             "price": "1.4",
...             "state": "PENDING",
...             "timeInForce": "GTC",
...             "tradeID": "1023",
...             "triggerCondition": "TRIGGER_DEFAULT",
...             "type": "TAKE_PROFIT"
...         },
...         "unrealizedPL": "-0.0002"
...     }
... }
```

Don't forget to use the Oanda definitions site for the keys above, concretely [HERE](http://developer.oanda.com/rest-live-v20/trades-df/) for trades.

#### Updating open trades

Suppose I want to secure profit (move stoploss) before the price meet the takeprofit level:

```python
>>> o.update_trade(own_id="EUR_USD_6", stoploss=1.13)
True
>>>
```

#### Closing open trades

```python
>>> o.close_trade(own_id="EUR_USD_6")
True
```

**Note**: Other trade methods are described in the [API reference][api-reference].

### Positions

#### Getting positions

Positions show cumulative profits and losses on both sides (LONG and SHORT) for each instrument.

```python
>>> o.get_positions()
... {
...     "lastTransactionID": "6381",
...     "positions": [
...         {
...             "instrument": "EUR_USD",
...             "long": {
...                 "pl": "-2.34608",
...                 "resettablePL": "-2.34608",
...                 "units": "0",
...                 "unrealizedPL": "0.00000"
...             },
...             "pl": "-2.34608",
...             "resettablePL": "-2.34608",
...             "short": {
...                 "pl": "0.00000",
...                 "resettablePL": "0.00000",
...                 "units": "0",
...                 "unrealizedPL": "0.00000"
...             },
...             "unrealizedPL": "0.00000"
...         },
...         {
...             "instrument": "USD_JPY",
...             ...
...         }
...     ]
... }
```

---

And this is the end of quickstart section. More methods you'll find in the [API Reference][api-reference] and next new methods are going to be implement, don't worry.
The future `1.0.0` will have everything necessary for automatic / algorithimic trading.

### Tips and tricks

#### Converting Oanda datetime to Python datetime object

Oanda provides datetime in RFC 3339 format which is incompatible with Python datetime object, so we need to do a bit more work to convert it:

```python
>>> import datetime 
>>>
>>> oanda_datetime = "2016-06-22T18:41:29.294265338Z"
>>> cut_it_off = oanda_datetime[:-4]
>>>
>>> datetime.datetime.strptime(cut_it_off, "%Y-%m-%dT%H:%M:%S.%f")
datetime.datetime(2016, 6, 22, 18, 41, 29, 294265)

[api-reference]: https://github.com/nait-aul/oandav20/blob/master/docs/api-reference.md

