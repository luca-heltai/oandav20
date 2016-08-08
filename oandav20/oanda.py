from typing import Any

import requests

from mixins.account import AccountMixin
from mixins.orders import OrdersMixin
from mixins.trades import TradesMixin
from mixins.pricing import PricingMixin


class Oanda(AccountMixin, OrdersMixin, TradesMixin, PricingMixin):
    """Oanda is the only (main) class, which should be used by user.

    It consist of several inherited mixins which extends funcionality of this
    class. Each mixin covers thematic endpoints, eg. one for orders handling,
    another for getting account information etc.

    Oanda allows to users to have 1 or more trading (sub)accounts. For those
    who manage only 1 may be too explicit to pass every time the account ID
    to methods for constructing a URL path. Moreover, there are endpoints
    where passing any account ID would lead to the same results.

    Therefore a 'default_id' attribute will be used for these situations unless
    the use user provide an different ID to the methods.

    Attributes:
        __base_url (str):
            Prefix for all endpoints.
        __client (object):
            Session object with HTTP persistent connection to the Oanda API
            server.
        default_id (str):
            Oanda account ID.
    """

    def __init__(self, environment: str, access_token: str, default_id: str) \
            -> None:
        """Initialize an instance of class Oanda.

        Arguments:
            environment (str):
                Accepts only value "DEMO" or "REAL".
            access_token (str):
                Access token for user authentication.
            default_id (str):
                Oanda account ID.

        Raises:
            ValueError:
                Value "DEMO" or "REAL" wasn't passed to the 'environment'
                parameter.
        """
        if environment == "DEMO":
            self.__base_url = "https://api-fxpractice.oanda.com/v3/accounts"
        elif environment == "REAL":
            self.__base_url = "https://api-fxtrade.oanda.com/v3/accounts"
        else:
            raise ValueError("Invalid environment '{}'.".format(environment))

        self.__client = requests.Session()
        self.__client.headers["Authorization"] = "Bearer " + access_token
        self.__client.headers["Content-Type"] = "application/json"

        self.default_id = default_id

    def send_request(self, endpoint: str, method: str = "GET", 
                     **kwargs: Any) -> requests.Response:
        """Send an HTTP request to the Oanda server.

        User may also use this method for accessing another endpoints which
        aren't covered in this package.

        Arguments:
            endpoint (str):
                Suffix of a URL.
            method (str, optional, default "GET"):
                HTTP method written in capital letters.
            **kwargs:
                Same keywords arguments like for 'request' object from
                'requests' package.

        Returns:
            HTTP Response object from 'requests' package.
        """
        url = self.__base_url + endpoint

        return self.__client.request(method, url, **kwargs)
