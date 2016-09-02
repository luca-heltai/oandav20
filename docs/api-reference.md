# API Rereference

## oandav20.oanda

### class oandav20.oanda.Oanda

Oanda is the main class responsible for interaction between a client
and the Oanda trading server.

It consists of several inherited mixins which extend its funcionality.
Each mixin covers an thematic endpoint, for example one for orders
handling, another for getting account information etc.

Oanda allows to users to have one or more trading accounts for different
base currency or leverage. For those who manage only one account may be
too explicit to pass every time the trading account ID to methods
(where required) for constructing a URL path.

Moreover, there are endpoints where passing any trading account ID would
lead to the same results. Therefore a 'default_id' attribute will be used
for these situations unless the use user provides an different ID to the
methods.

**Attributes:**

- base_url (str):
    - Base url alias prefix for all endpoints.
- client (requests.Session):
    - Session object with HTTP persistent connection to the Oanda API
server.
- default_id (str):
    - Default Oanda trading account ID.

#### method \_\_init\_\_

Initialize an instance of class Oanda.

**Arguments:**

- environment (str)
    - Trading environment, accepts only value "DEMO" or "REAL".
- access_token (str)
    - Access token for user authentication.
- default_id (str)
    - Default Oanda trading account ID.

**Raises:**

- ValueError:
    - Value "DEMO" or "REAL" wasn't passed to the 'environment'
parameter.

#### method send_request

Send an HTTP request to the Oanda trading server.

User may also use this method for accessing another endpoints which
aren't covered in this package.

**Arguments:**

- endpoint (str)
    - Suffix for a URL.
- method (str, optional, default 'GET')
    - HTTP method written in capital letters.
- kwargs (Any)
    - Same keywords arguments like for an 'request' object from a
'requests' package.

**Returns:**
    HTTP Response object from the 'requests' package.

## oandav20.mixins.account

### class oandav20.mixins.account.AccountMixin

Methods in the AccountMixin class handles the account endpoints.

#### method get_available_accounts

Get list of accounts for the current access token.

**Returns:**
    JSON object (dict) with the accounts IDs.

Example:

```python
{
    "accounts": [
        {
            "id": "<ACCOUNT ID>",
            "tags": []
        },
        {
            ...
        }
    ]
}
```

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.

#### method get_account

Get full account details.

This option includes information about pending orders, open trades and
closed positions.

**Arguments:**

- account_id (str, optional, default '')
    - Oanda trading account ID, otherwise 'default_id' will be used.

**Returns:**
    JSON object (dict) with the full account details.

Example:

```python
{
    "account": {
        "NAV": "43650.78835",
        "alias": "My New Account #2",
        "balance": "43650.78835",
        "createdByUserID": <USERID>,
        "createdTime": "2015-08-12T18:21:00.697504698Z",
        "currency": "CHF",
        "hedgingEnabled": false,
        "id": "<ACCOUNT>",
        "lastTransactionID": "6356",
        "marginAvailable": "43650.78835",
        "marginCloseoutMarginUsed": "0.00000",
        "marginCloseoutNAV": "43650.78835",
        "marginCloseoutPercent": "0.00000",
        "marginCloseoutPositionValue": "0.00000",
        "marginCloseoutUnrealizedPL": "0.00000",
        "marginRate": "0.02",
        "marginUsed": "0.00000",
        "openPositionCount": 0,
        "openTradeCount": 0,
        "orders": [],
        "pendingOrderCount": 0,
        "pl": "-56034.41199",
        "positionValue": "0.00000",
        "positions": [
            {
                "instrument": "EUR_GBP",
                "long": {
                    "pl": "-21.81721",
                    "resettablePL": "-21.81721",
                    "units": "0",
                    "unrealizedPL": "0.00000"
                },
                "pl": "-21.81721",
                "resettablePL": "-21.81721",
                "short": {
                    "pl": "0.00000",
                    "resettablePL": "0.00000",
                    "units": "0",
                    "unrealizedPL": "0.00000"
                },
                "unrealizedPL": "0.00000"
            },
            {
                ...
            }
        ],
        "resettablePL": "-56034.41199",
        "trades": [],
        "unrealizedPL": "0.00000",
        "withdrawalLimit": "43650.78835"
    },
    "lastTransactionID": "6356"
}
```

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.

#### method get_account_summary

Get short variant of account details.

In this option are excluded pendings orders, open trades, closed
positions.

**Arguments:**

- account_id (str, optional, default '')
    - Oanda trading account ID, otherwise 'default_id' will be used.

**Returns:**
    JSON object (dict) with the account summary details.

Example:

```python
{
    "account": {
        "NAV": "43650.78835",
        "alias": "My New Account #2",
        "balance": "43650.78835",
        "createdByUserID": <USERID>,
        "createdTime": "2015-08-12T18:21:00.697504698Z",
        "currency": "CHF",
        "hedgingEnabled": false,
        "id": "<ACCOUNT>",
        "lastTransactionID": "6356",
        "marginAvailable": "43650.78835",
        "marginCloseoutMarginUsed": "0.00000",
        "marginCloseoutNAV": "43650.78835",
        "marginCloseoutPercent": "0.00000",
        "marginCloseoutPositionValue": "0.00000",
        "marginCloseoutUnrealizedPL": "0.00000",
        "marginRate": "0.02",
        "marginUsed": "0.00000",
        "openPositionCount": 0,
        "openTradeCount": 0,
        "pendingOrderCount": 0,
        "pl": "-56034.41199",
        "positionValue": "0.00000",
        "resettablePL": "-56034.41199",
        "unrealizedPL": "0.00000",
        "withdrawalLimit": "43650.78835"
    },
    "lastTransactionID": "6356"
}
```

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.

#### method get_instruments

Get details for one or more or all tradeable instruments.

If a user won't pass any instrument code(s) to the 'instruments'
parameter, then will be returned details for all instruments.

**Arguments:**

- instruments (List[str], optional, default [])
    - Code of instrument(s).
- account_id (str, optional, default '')
    - Oanda trading account ID, otherwise 'default_id' will be used.

**Returns:**
    JSON object (dict) with the instrument(s) details.

Example:

```python
{
    "instruments": [
        {
            "displayName": "USD/THB",
            "displayPrecision": 3,
            "marginRate": "0.05",
            "maximumOrderUnits": "100000000",
            "maximumPositionSize": "0",
            "maximumTrailingStopDistance": "100.000",
            "minimumTradeSize": "1",
            "minimumTrailingStopDistance": "0.050",
            "name": "USD_THB",
            "pipLocation": -2,
            "tradeUnitsPrecision": 0,
            "type": "CURRENCY"
        },
        {
            ...
        }
    ]
}
```

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- ValueError:
    - Invalid instrument code(s) passed to the 'instruments'
parameter.

#### method configure_account

Configure the given trading account.

By this method is possible only configure margin rate alias minimum
required margin per trade. Allowed values are below in the 'Minimum
margin' column (without the percentage sign).

| Leverage ratio | Minimum margin | Margin rate |
| --- | --- | --- |
| 100:1 | 1 % | 0.01 |
| 50:1 | 2 % | 0.02 |
| 40:1 | 2.5 % | 0.025 |
| 30:1 | 3.3 % | 0.0333 |
| 20:1 | 5 % | 0.05 |
| 10:1 | 10 % | 0.1 |

**Arguments:**

- margin (Union[float, int])
    - Minimum margin per trade expressed in the percentage.

**Returns:**
    True if the account was configured successfully.

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- ValueError:
    - Invalid

## oandav20.mixins.orders

### class oandav20.mixins.orders.OrdersMixin

Methods in the OrdersMixin class handles the orders endpoints.

#### method create_order

Create an order for the given instrument with specified parameters.

If a user didn't place own ID then he / she must remember order ID
created by Oanda and himself / herself check if the order is still
pending or filled.

Therefore I highly recommend to use own ID, for example "EUR_USD_1"
which be used both for orders and trades.

**Arguments:**

- order_type (str)
    - Type of order, accepting only value "MARKET", "LIMIT" or
"STOP".
- instrument (str)
    - Code of instrument.
- side (str)
    - Side of order, accepting only value "BUY" or "SELL".
- units (int)
    - Size of order.
- price (float, optional, default 0.0)
    - Price level for orders "LIMIT" and "STOP".
- price_bound (float, optional, default 0.0)
    - The worse market price that may be filled, goes only for "STOP"
order.
- time_in_force (str, optional, default '')
    - How long should the order remain pending. Accepting only codes
"FOK" or "IOC" for the "MARKET" order, for the rest "GTC" or
"GFD" codes. "FOK" is default for the "MARKET" type and "GTC"
for the waiting types.
- stoploss (float, optional, default 0.0)
    - Stoploss level.
- takeprofit (float, optional, default 0.0)
    - Takeprofit level.
- own_id (str, optional, default '')
    - Own ID used for this order and if filled, then also for
the open trade.
- tag (str, optional, default '')
    - User tag.
- comment (str, optional, default '')
    - User comment.
- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    True if the order was created as specified and user used own ID or
    returns order ID created by Oanda.

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Argument for the 'price' parameter is required, if the order
type is either "LIMIT" or "STOP".
- ValueError:
    1. Invalid order type passed to the 'order_type' parameter.
    2. Invalid instrument code passed to the 'instrument'
parameter.
    3. Invalid side passes to the 'side' parameter.
    4. Invalid size of units passed to the 'units' parameter.
    5. Invalid TimeInForce code for the given order type passed
to the 'time_in_force' parameter.

#### method create_market_order

Alias for the 'create_order' with first argument "MARKET".

**Arguments:**

- args (Any)
    - Same args like for the 'create_order'
- kwargs (Any)
    - Same kwargs like for the 'create_order'

**Returns:**
    Call the 'create_order' method with first argument "MARKET".

#### method create_limit_order

Alias for the 'create_order' with first argument "LIMIT".

**Arguments:**

- args (Any)
    - Same args like for the 'create_order'
- kwargs (Any)
    - Same kwargs like for the 'create_order'

**Returns:**
    Call the 'create_order' method with first argument "LIMIT".

#### method create_stop_order

Alias for the 'create_order' with first argument "STOP".

**Arguments:**

- args (Any)
    - Same args like for the 'create_order'
- kwargs (Any)
    - Same kwargs like for the 'create_order'

**Returns:**
    Call the 'create_order' method with first argument "STOP".

#### method get_order

Get details for the given order ID.

User may choose if the order details will be obtained by Oanda ID or
its ID.

**Arguments:**

- order_id (int, optional, default 0)
    - Order ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    JSON object (dict) with the order details.

Example:

```python
{
    "lastTransactionID": "6375",
    "order": {
        "clientExtensions": {
            "comment": "New idea for trading",
            "id": "my_order_100",
            "tag": "strategy_9"
        },
        "createTime": "2016-06-22T18:41:29.294265338Z",
        "id": "6375",
        "instrument": "EUR_CAD",
        "partialFill": "DEFAULT_FILL",
        "positionFill": "POSITION_DEFAULT",
        "price": "1.30000",
        "replacesOrderID": "6373",
        "state": "PENDING",
        "timeInForce": "GTC",
        "triggerCondition": "TRIGGER_DEFAULT",
        "type": "STOP",
        "units": "10000"
    }
}
```

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'order_id' or 'own_id'
parameter.

#### method get_all_orders

Get list of all pending orders.

**Arguments:**

- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    JSON object (dict) with the pending orders details.

Example:

```python
{
    "lastTransactionID": "6375",
    "orders": [
        {
            "clientExtensions": {
                "comment": "New idea for trading",
                "id": "my_order_100",
                "tag": "strategy_9"
            },
            "createTime": "2016-06-22T18:41:29.294265338Z",
            "id": "6375",
            "instrument": "EUR_CAD",
            "partialFill": "DEFAULT_FILL",
            "positionFill": "POSITION_DEFAULT",
            "price": "1.30000",
            "replacesOrderID": "6373",
            "state": "PENDING",
            "timeInForce": "GTC",
            "triggerCondition": "TRIGGER_DEFAULT",
            "type": "STOP",
            "units": "10000"
        },
        {
            ...
        }
    ]
}
```

**Raises:**

- HTTPError:
    - HTTP response status code is 4xx or 5xx.

#### method update_order

Update values for the specific pending order.

User may update only values such as 'price', 'stoploss', 'takeprofit'
etc., not change instrument or even order type / side. For these
situations must close the pending order himself / herself and create
new one.

**Arguments:**

- order_id (int, optional, default 0)
    - Order ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- price (float, optional, default 0.0)
    - Price level for waiting orders.
- price_bound (float, optional, default 0.0)
    - The worse market price that may be filled, goes only for "STOP"
order.
- stoploss (float, optional, default 0.0)
    - Stoploss level.
- takeprofit (float, optional, default 0.0)
    - Maximal profit.
- units (int, optional, default 0)
    - Order size.
- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    True if used own ID or new Oanda order ID if the old Oanda order
    ID was used.

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'order_id' or 'own_id'
parameter.

#### method update_order_extensions

Update client extensions for the given order.

User may choose if wants to get the order by Oanda ID or its ID.

**Note:**
    New own ID or tag should be used very rarely in my opinion.

**Arguments:**

- order_id (int, optional, default 0)
    - Order ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- new_own_id (str, optional, default '')
    - New own ID which will replace existing own ID.
- tag (str, optional, default '')
    - New tag.
- comment (str, optional, default '')
    - New comment.
- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    True, if the trade was succesfully updated.

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'trade_id' or 'own_id'
parameter.

#### method cancel_order

Cancel the given pending order.

User may choose if the order details will be obtained by Oanda ID or
its ID.

**Arguments:**

- order_id (int, optional, default 0)
    - Order ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- account_id (None, optional, default '')
    - Oanda trading account ID.

**Returns:**
    True, if the pending order was cancelled.

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'order_id' or 'own_id'
parameter.

#### method cancel_filtered_orders

Cancel the filtered pending orders if there are any.

This method is very useful for situations where is important to
cancel all pending orders which relate to USD currency before news are
released.

**Arguments:**

- order_ids (List[int], optional, default [])
    - Order IDs provided by Oanda.
- own_ids (List[str], optional, default [])
    - Own orders IDs (via 'own_id').
- instrument (str, optional, default '')
    - Instrument code or also single currency code.

**Raises:**

- TypeError:
    - Missing argument either for the 'order_ids' or 'own_ids' or
'instrument' parameter.

**Todo:**

- [ ] refactor to async

#### method cancel_all_orders

Cancel all pending orders if there are any.

**Arguments:**

- account_id (str, optional, default '')
    - Oanda trading account ID.

**Todo:**

- [ ] refactor to async

## oandav20.mixins.positions

### class oandav20.mixins.positions.PositionsMixin

Methods in the PricingMixin class handles the pricing endpoints.

#### method get_positions

Get list of all positions details (finished trades).

**Arguments:**

- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    JSON object (dict) with all the positions details.

Example:

```python
{
    "lastTransactionID": "6381",
    "positions": [
        {
            "instrument": "CHF_JPY",
            "long": {
                "pl": "-2.34608",
                "resettablePL": "-2.34608",
                "units": "0",
            "unrealizedPL": "0.00000"
            },
            "pl": "-2.34608",
            "resettablePL": "-2.34608",
            "short": {
                "pl": "0.00000",
                "resettablePL": "0.00000",
                "units": "0",
                "unrealizedPL": "0.00000"
            },
            "unrealizedPL": "0.00000"
        },
        {
            ...
        }
    ]
}
```

**Raises:**

- requets.HTTPError:
    - HTTP response status code is 4xx or 5xx.

## oandav20.mixins.pricing

### class oandav20.mixins.pricing.PricingMixin

Methods in the PricingMixin class handles the pricing endpoints.

#### method get_pricing

Get pricing information for 1 or more instruments.

**Arguments:**

- instruments (List[str])
    - Code of instrument(s).

**Returns:**
    JSON object (dict) with the pricing information.

Example:

```python
{
    "prices": [
        {
            "asks": [
                {
                    "liquidity": 10000000,
                    "price": "1.13028"
                },
                {
                    ...
                }
            ],
            "bids": [
                {
                    "liquidity": 10000000,
                    "price": "1.13015"
                },
                {
                    ...
                }
            ],
            "closeoutAsk": "1.13032",
            "closeoutBid": "1.13011",
            "instrument": "EUR_USD",
            "quoteHomeConversionFactors": {
                "negativeUnits": "0.95904000",
                "positiveUnits": "0.95886000"
            },
            "status": "tradeable",
            "time": "2016-06-22T18:41:36.201836422Z",
            "unitsAvailable": {
                "default": {
                    "long": "2013434",
                    "short": "2014044"
                },
                "openOnly": {
                    "long": "2013434",
                    "short": "2014044"
                },
                "reduceFirst": {
                    "long": "2013434",
                    "short": "2014044"
                },
                "reduceOnly": {
                    "long": "0",
                    "short": "0"
                }
            }
        },
        {
            ...
        }
    ]
}
```

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- ValueError:
    - Invalid instrument code passed to the 'instruments' parameter.

## oandav20.mixins.trades

### class oandav20.mixins.trades.TradesMixin

Methods in the TradesMixin class handles the trades endpoints.

#### method get_trade

Get details for the given trade.

The trade may be either open or closed. User may choose if wants to
update the trade by Oanda ID or own ID.

**Arguments:**

- trade_id (int, optional, default 0)
    - Trade ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- account_id (str, optional, default '')
    - Oanda trading account ID

**Returns:**
    JSON object (dict) with the trade details.

Example:

```python
{
    "lastTransactionID": "1025",
    "trade": {
        "clientExtensions": {
            "id": "USD_CHF_95",
        },
        "currentUnits": "1",
        "financing": "0.0000",
        "id": "1023",
        "initialUnits": "1",
        "instrument": "USD_CHF",
        "openTime": "2016-08-17T15:21:29.306846600Z",
        "price": "0.96308",
        "realizedPL": "0.0000",
        "state": "OPEN",
        "stopLossOrder": {
            "createTime": "2016-08-17T15:21:29.715039917Z",
            "id": "1025",
            "price": "0.95287",
            "state": "PENDING",
            "timeInForce": "GTC",
            "tradeID": "1023",
            "triggerCondition": "TRIGGER_DEFAULT",
            "type": "STOP_LOSS"
        },
        "takeProfitOrder": {
            "createTime": "2016-08-17T15:21:29.715039917Z",
            "id": "1024",
            "price": "0.97287",
            "state": "PENDING",
            "timeInForce": "GTC",
            "tradeID": "1023",
            "triggerCondition": "TRIGGER_DEFAULT",
            "type": "TAKE_PROFIT"
        },
        "unrealizedPL": "-0.0002"
    }
}
```


**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'trade_id' or 'own_id'
parameter.

#### method get_all_trades

Get list of all open trades.

**Arguments:**

- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    JSON object (dict) with the open trades details.

Example:

```python
{
    "lastTransactionID": "6397",
    "trades": [
        {
            "clientExtensions": {
                "id": "my_eur_usd_trade"
            },
            "currentUnits": "100",
            "financing": "0.00000",
            "id": "6395",
            "initialUnits": "100",
            "instrument": "EUR_USD",
            "openTime": "2016-06-22T18:41:48.258142231Z",
            "price": "1.13033",
            "realizedPL": "0.00000",
            "state": "OPEN",
            "unrealizedPL": "-0.01438"
        },
        {
            ...
        }
    ]
}
```

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.

#### method update_trade

Update editable values (see the parameters) for the given order.

User may choose if wants to update the trade by Oanda ID or its ID.

**Note:**
    For removing / erasing values you need to pass negative float
    number.

**Arguments:**

- trade_id (int, optional, default 0)
    - Trade ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- stoploss (float, optional, default 0.0)
    - Stoploss level.
- takeprofit (float, optional, default 0.0)
    - Takeprofit level.
- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    True, if the trade update was succesful.

**Raises:**

- requets.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'trade_id' or 'own_id'
parameter.

#### method update_trade_extensions

Update client extensions for the given trade.

User may choose if wants to get the trade by Oanda ID or its ID.

**Note:**
    New own ID or tag should be used very rarely in my opinion.

**Arguments:**

- trade_id (int, optional, default 0)
    - Trade ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- tag (str, optional, default '')
    - Trade tag.
- comment (str, optional, default '')
    - Trade comment.

**Returns:**
    True, if the trade was succesfully updated.

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'trade_id' or 'own_id'
parameter.

#### method close_trade

Close fully or partially the given open trade.

User may choose if wants to close the trade by Oanda ID or its ID.

**Arguments:**

- trade_id (int, optional, default 0)
    - Trade ID provided by Oanda.
- own_id (str, optional, default '')
    - Own ID.
- units (int, optional, default 0)
    - How many units should be closed. If empty then all units will
be used.
- account_id (str, optional, default '')
    - Oanda trading account ID.

**Returns:**
    True if the trade was closed properly.

**Raises:**

- requests.HTTPError:
    - HTTP response status code is 4xx or 5xx.
- TypeError:
    - Missing argument either for the 'trade_id' or 'own_id'
parameter.

#### method close_filtered_trades

Close the filtered trades.

**Arguments:**

- trade_ids (List[int], optional, default [])
    - Trade IDs provided by Oanda.
- own_ids (List[str], optional, default [])
    - Own trade IDs.
- instrument (str, optional, default '')
    - Instrument code or also single currency code.

**Raises:**

- TypeError:
    - Missing argument either for the 'trade_ids' or 'own_ids' or
'instrument' parameter.

**Todo:**

- [ ] refactor to async

#### method close_all_trades

Close all the open trades if there are any.

**Arguments:**

- account_id (str, optional, default '')
    - Oanda trading account ID.

**Todo:**

- [ ] refactor async

## oandav20.testing.testcase

### class oandav20.testing.testcase.TestCase

Custom TestCase class for unittesting package Oandav20.

#### method setUpClass

Create an HTTP session connection with the Oanda server.

#### method tearDownClass

Close all open trades and pending orders if any exist and close the
HTTP session connection.
