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

## Features

- pass only one Oanda account ID and remember it (useful, if you manage only one account)
- cancel filtered / all pending orders at once
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

## Development status

The lastest version 0.1.0 covers the minimum to run and keep an automatic trading software in my opinion.

The stable/production 1.0.0 will be released as soon as:

1. Oanda implement promised features such as streaming, pricing history and tools from Oanda Forex Labs
2. I create an AOS to know which functions are needed and which not. 

## Documentation

Full documentation will be placed in the [Wiki](https://github.com/nait-aul/oandav20/wiki) section here on GitHub.

First I need to write a documentation generator for my docstrings style (inspired by Google Docstring Style).

## Contribution

If you've found a bug or want to suggest new features, please feel free to use [Issue Tracker](https://github.com/nait-aul/oandav20/issues).

## Changelog

All new features, changes and bug fixes of each version is convered in the [CHANGELOG](https://github.com/nait-aul/oandav20/blob/master/CHANGELOG.md) file.
 
## License

Oandav20 is licensed under the terms of the MIT License (see the [LICENSE](https://github.com/nait-aul/oandav20/blob/master/LICENSE) file)
