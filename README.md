# Oandav20

`oandav20` is an unofficial Python SDK for [Oanda v20 REST API](http://developer.oanda.com/rest-live-v20/introduction/) in planning mode.

```python
>>> from oandav20 import Oanda
>>>
>>> o = Oanda("DEMO", "oanda_access_token", "oanda_account_id") 
>>> o.create_order("MARKET", "EUR_USD", "BUY", 10000, own_id="EUR_USD_1")
True
>>> o.close_trade(own_id="EUR_USD_1")
True
>>>
>>> # Close the HTTP session connection with Oanda
>>> o.client.close()
```

## Installation

To install `oandav20` you need Python 3.5.x and above because of using type hints (new feature in Python 3.5).

```
pip install oandav20
```

## Features

- pass only one Oanda account ID and remember it (useful, if you manage only one account)
- update pending orders without closing one and creating one (reusing the previous order details)
- cancel filtered / all pending orders at once (eg. cancel all fx pairs with the "USD")
- close filtered / all open trades at once

Intended to implement:

- configuration file
- async support
- pausing waiting orders
- cover more useful endpoints
- and other ideas which may come up ...

Intended related projects:

- data visualization (web page and native mobile application)
- pattern detection

## Documentation

Full documentation is placed in the [docs](https://github.com/nait-aul/oandav20/tree/master/docs) folder.

API Reference will be added as soon as I write a documentation generator for my docstrings style (slightly modified Napoleon style but output to Markdown.).

## Development status

The latest version 0.2.0 covers the minimum to run and keep an automatic trading software in my opinion.

The stable/production 1.0.0 will be released as soon as:

1. Oanda implement promised features such as streaming, pricing history and tools from Oanda Forex Labs
2. I create an AOS to know which methods are needed and which not. 

## Contribution

If you've found a bug or want to suggest new features, please feel free to use [Issue Tracker](https://github.com/nait-aul/oandav20/issues).

## Changelog

All new features, changes and bug fixes of each versions are convered in the [CHANGELOG](https://github.com/nait-aul/oandav20/blob/master/CHANGELOG.md).
 
## License

`oandav20` is licensed under the terms of the MIT License, for more details see the [LICENSE](https://github.com/nait-aul/oandav20/blob/master/LICENSE).
