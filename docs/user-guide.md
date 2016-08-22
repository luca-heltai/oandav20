# User guide

## Introduction

Oandav20 is designed to be rather SDK than ordinary REST API wrapper which may explicitly cover every possible endpoints and maybe you never use it at all.

Unlike the wrappers this package extends the default Oanda API by more useful methods which in fact combine several endpoints at once.

For example:

- update a pending order without closing one and creating new one
- bulk cancel all pendings orders or filtered (eg. only the fx pairs which contain "USD")
- bulk close all open trades or filtered

There is also time-saving feature:

- remember trading account ID and reuse it in methods where required

**Note**: Oandav20 is still in planning mode and therefore there may be API breaks during development before reaching the stable/production 1.0.0 version.

## Installation

If you haven't installed it yet and have Python 3.5.x version and above, then do:

```
pip install oandav20
```

## Quickstart

### Oanda object

The main object for interaction with the Oanda API server is `Oanda` class:

```python
from oandav20 import Oanda

o = Oanda("environment", "access_token", "default_id")
```

As you may see, `Oanda` requires 3 arguments:

1. environment = "DEMO" or "REAL"
2. access_token = your generated access token which will be used for authentication (navigate to you Oanda account dashboard and click to `Manage API Access`)
3. default_id = your default trading accout ID (in the dashboard click to `Manage Funds`)

Before we start calling methods on the `o` object, I would like to tell you what is really happening in background.

By initialization the `o` object is is prepared one persistent TCP/IP connection with the Oanda server. Every time you will call a method, an HTTP request is send and waiting for response.

Be aware thath maximum allowed number of requests is 30 per minute. Any extra requests will be ignored.

When it comes to finish trading, it would be very pleasant if you close the persistent HTTP connection (session):

```python
o.client.close()
```

