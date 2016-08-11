class PositionsMixin:
    """Methods in the PricingMixin class handles the pricing endpoints."""

    def get_positions(self, account_id: str = "") -> dict:
        """Get list of all positions details (finished trades).

        Arguments:
            account_id:
                Oanda trading account ID.

        Returns:
            JSON object (dict) with all the positions details.

        Example:
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

        Raises:
            requets.HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/positions".format(account_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()
