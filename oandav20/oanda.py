from typing import Any

import requests

from .mixins.account import AccountMixin
from .mixins.orders import OrdersMixin
from .mixins.trades import TradesMixin
from .mixins.positions import PositionsMixin
from .mixins.pricing import PricingMixin


class Oanda(AccountMixin, OrdersMixin, TradesMixin, PositionsMixin,
            PricingMixin):
    """Oanda is the main class responsible for interaction between a client
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

    Attributes:
        base_url:
            Base url alias prefix for all endpoints.
        client:
            Session object with HTTP persistent connection to the Oanda API
            server.
        default_id:
            Default Oanda trading account ID.
    """

    def __init__(self, environment: str, access_token: str, default_id: str) \
            -> None:
        """Initialize an instance of class Oanda.

        Arguments:
            environment:
                Trading environment, accepts only value "DEMO" or "REAL".
            access_token:
                Access token for user authentication.
            default_id:
                Default Oanda trading account ID.

        Raises:
            ValueError:
                Value "DEMO" or "REAL" wasn't passed to the 'environment'
                parameter.
        """
        if environment == "DEMO":
            self.base_url = "https://api-fxpractice.oanda.com/v3/accounts"
        elif environment == "REAL":
            self.base_url = "https://api-fxtrade.oanda.com/v3/accounts"
        else:
            raise ValueError("Invalid environment '{}'.".format(environment))

        self.client = requests.Session()
        self.client.headers["Authorization"] = "Bearer " + access_token
        self.client.headers["Content-Type"] = "application/json"

        self.default_id = default_id

    def send_request(self, endpoint: str, method: str = "GET",
                     **kwargs: Any) \
            -> requests.Response:
        """Send an HTTP request to the Oanda trading server.

        User may also use this method for accessing another endpoints which
        aren't covered in this package.

        Arguments:
            endpoint:
                Suffix for a URL.
            method:
                HTTP method written in capital letters.
            **kwargs:
                Same keywords arguments like for an 'request' object from a
                'requests' package.

        Returns:
            HTTP Response object from the 'requests' package.
        """
        url = self.base_url + endpoint

        return self.client.request(method, url, **kwargs)
