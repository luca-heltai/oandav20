from .account import INSTRUMENTS


class PositionsMixin:
    """Methods in the PricingMixin class handles the pricing endpoints."""

    def get_positions(self, account_id: str = "") -> dict:
        """Get list of all positions details (finished trades).

        Arguments:
            account_id (str, optional):
                Oanda account ID.

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
            HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/positions".format(account_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_filtered_positions(self, instrument: str, account_id: str = "") \
            -> dict:
        """Get filtered positions by instrument.

        Arguments:
            instrument (str):
                Code of instrument.
            account_id (str, optional):
                Oanda account ID.

        Returns:
            JSON object (dict) with the filtered positions by intrument.

        Example:
            .

        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            ValueError:
                Invalid instrument code passed to the 'instrument' parameter.
        """
        account_id = account_id or self.default_id

        if instrument not in INSTRUMENTS.values():
            raise ValueError("Invalid instrument code '{}'.".format(
                instrument))

        pass
