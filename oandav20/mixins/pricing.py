from typing import List

from oandav20.mixins.account import INSTRUMENTS


class PricingMixin:
    """Methods in the PricingMixin class handles the pricing endpoints."""

    def get_pricing(self, instruments: List[str]) -> dict:
        """Get pricing information for 1 or more instruments.

        Arguments:
            instruments:
                Code of instrument(s).

        Returns:
            JSON object (dict) with the pricing information.

        Example:
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

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            ValueError:
                Invalid instrument code passed to the 'instruments' parameter.
        """
        account_id = self.default_id
        endpoint = "/{}/pricing".format(account_id)

        for code in instruments:
            if code in INSTRUMENTS.values():
                continue
            else:
                raise ValueError("Invalid instrument code '{}'.".format(code))

        url_params = {"instruments": ",".join(instruments)}
        response = self.send_request(endpoint, params=url_params)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()
