from typing import List

from .account import INSTRUMENTS


class TradesMixin:
    """Methods in the TradesMixin class handles the trades endpoints."""

    def get_trade(self, trade_id: int = 0, own_id: str = "",
                  account_id: str = "") \
            -> dict:
        """Get details for the given trade.

        The trade may be either open or closed. User may choose if wants to
        update the trade by Oanda ID or own ID.

        Arguments:
            trade_id:
                Trade ID provided by Oanda.
            own_id:
                Own ID.
            account_id:
                Oanda trading account ID

        Returns:
            JSON object (dict) with the trade details.

        Example:
            {
                "lastTransactionID": "6397",
                "trade": {
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
                }
            }

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'trade_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not trade_id and not own_id:
            raise TypeError("Missing argument either for the 'trade_id' or "
                            "'own_id'.")

        if own_id:
            own_id = "@" + own_id

        used_id = trade_id or own_id
        endpoint = "/{0}/trades/{1}".format(account_id, used_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_filtered_trades(self, trade_ids: List[int] = [],
                            instrument: str = "", account_id: str = "") \
            -> dict:
        """Get list of filtered open trades.

        There are picked only the two filters (see parameters) which I
        consider as reasonable.

        Arguments:
            trade_ids:
                List of Oanda trade IDs, not own trade IDs.
            instrument:
                Code of single instrument.
            account_id:
                Oanda trading account ID.

        Returns:
            JSON object (dict) with the filtered open trades details.

        Example:
            {
                "lastTransactionID": "6397",
                "trades": [
                    {
                        "currentUnits": "-600",
                        "financing": "0.00000",
                        "id": "6397",
                        "initialUnits": "-600",
                        "instrument": "USD_CAD",
                        "openTime": "2016-06-22T18:41:48.262344782Z",
                        "price": "1.28241",
                        "realizedPL": "0.00000",
                        "state": "OPEN",
                        "unrealizedPL": "-0.08525"
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
                Invalid instrument code passed to the 'instrument' parameter.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/trades".format(account_id)
        url_params = {}

        if trade_ids:
            joined_ids = ",".join([str(id) for id in trade_ids])
            url_params["ids"] = joined_ids

        if instrument:
            if instrument in INSTRUMENTS.values():
                url_params["instrument"] = instrument
            else:
                raise ValueError("Invalid instrument code ''.".format(
                    instrument))

        response = self.send_request(endpoint, params=url_params)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_all_trades(self, account_id: str = "") -> dict:
        """Get list of all open trades.

        Arguments:
            account_id:
                Oanda trading account ID.

        Returns:
            JSON object (dict) with the open trades details.

        Example:
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

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/openTrades".format(account_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def update_trade(self, trade_id: int = 0, own_id: str = "",
                     stoploss: float = 0.0, takeprofit: float = 0.0,
                     account_id: str = "") \
            -> bool:
        """Create / update / remove values for the given order, eg. stoploss.

        User may choose if wants to update the trade by Oanda ID or its ID.

        Note:
            For removing / erasing values you need to pass negative float
            number.

        Arguments:
            trade_id:
                Trade ID provided by Oanda.
            own_id:
                Own ID.
            stoploss:
                Stoploss level.
            takeprofit:
                Takeprofit level.
            account_id:
                Oanda trading account ID.

        Returns:
            True, if the trade update was succesful.

        Raises:
            requets.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'trade_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not trade_id and not own_id:
            raise TypeError("Missing argument either for the 'trade_id' or "
                            "'own_id'.")

        if own_id:
            own_id = "@" + own_id

        used_id = trade_id or own_id
        endpoint = "/{0}/orders/{1}".format(account_id, used_id)
        request_body = {}

        if stoploss:
            if stoploss < 0.0:
                stoploss = 0

            request_body["stopLoss"] = {
                "price": str(stoploss),
                "timeInForce": "GTC"
            }

        if takeprofit:
            if takeprofit < 0.0:
                takeprofit = 0

            request_body["takeProfit"] = {
                "price": str(takeprofit),
                "timeInForce": "GTC"
            }

        response = self.send_request(endpoint, "PUT", json=request_body)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 201

    def update_trade_extensions(self, trade_id: int = 0, own_id: str = "",
                                new_own_id: str = "", tag: str = "",
                                comment: str = "", account_id: str = "") \
            -> bool:
        """Update client extensions for the given trade.

        User may choose if wants to get the trade by Oanda ID or its ID.

        Note:
            New own ID or tag should be used very rarely in my opinion.

        Arguments:
            trade_id:
                Trade ID provided by Oanda.
            own_id:
                Own ID.
            new_own_id:
                New own ID which will replace existing own ID.
            tag:
                Trade tag.
            comment:
                Trade comment.

        Returns:
            True, if the trade was succesfully updated.

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'trade_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not trade_id and not own_id:
            raise TypeError("Missing argument either for the 'trade_id' or "
                            "'own_id'.")

        if own_id:
            own_id = "@" + own_id

        used_id = trade_id or own_id
        endpoint = \
            "/{0}/trades/{1}/clientExtensions".format(account_id, used_id)
        request_body = {"clientExtensions": {}}

        if new_own_id:
            request_body["clientExtensions"]["id"] = new_own_id

        if tag:
            request_body["clientExtensions"]["tag"] = tag

        if comment:
            request_body["clientExtensions"]["comment"] = comment

        response = self.send_request(endpoint, "PUT", json=request_body)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 200

    def close_trade(self, trade_id: int = 0, own_id: str = "", units: int = 0,
                    account_id: str = "") \
            -> bool:
        """Close fully or partially the given open trade.

        User may choose if wants to close the trade by Oanda ID or its ID.

        Arguments:
            trade_id:
                Trade ID provided by Oanda.
            own_id:
                Own ID.
            units:
                How many units should be closed. If empty then all units will
                be used.
            account_id:
                Oanda trading account ID.

        Returns:
            True if the trade was closed properly.

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'trade_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not trade_id and not own_id:
            raise TypeError("Missing argument either for the 'trade_id' or "
                            "'own_id'.")

        if own_id:
            own_id = "@" + own_id

        used_id = trade_id or own_id
        endpoint = "/{0}/trades/{1}/close".format(account_id, used_id)

        if units:
            request_body = {"units": str(units)}
            response = self.send_request(endpoint, "PUT", json=request_body)
        else:
            response = self.send_request(endpoint, "PUT")

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 200

    def close_filtered_trades(self, trade_ids: List[int] = [],
                              own_ids: List[str] = [], instrument: str = "",
                              account_id: str = "") \
            -> None:
        """Close the filtered trades.

        Arguments:
            trade_ids:
                Trade IDs provided by Oanda.
            own_ids:
                Own trade IDs.
            instrument:
                Instrument code or also single currency code.

        Raises:
            TypeError:
                Missing argument either for the 'trade_ids' or 'own_ids' or
                'instrument' parameter.

        Todo:
            - refactor to async
        """
        account_id = account_id or self.default_id

        if not trade_ids or not own_ids or not instrument:
            raise TypeError("Missing argument either for the 'trade_ids' or "
                            "'own_ids' or 'instrument'.")

        open_trades = self.get_all_trades(account_id)

        if open_trades["trades"]:
            if trade_ids:
                for id in trade_ids:
                    self.close_trade(id, account_id=account_id)

                return

            if own_ids:
                for id in own_ids:
                    self.close_trade(own_id=id, account_id=account_id)

                return

            if instrument:
                trades_dict = \
                    {int(trade["id"]): trade["instrument"] for trade in
                     open_trades["trades"]}

                for key, value in trades_dict.items():
                    if instrument in trades_dict[key]:
                        self.close_trade(key, account_id=account_id)

                return

    def close_all_trades(self, account_id: str = "") -> None:
        """Close all the open trades if there are any.

        Arguments:
            account_id:
                Oanda trading account ID.

        Todo:
            - refactor async
        """
        account_id = account_id or self.default_id
        open_trades = self.get_all_trades(account_id)

        if open_trades["trades"]:
            trade_ids = \
                [int(trade["id"]) for trade in open_trades["trades"]]

            for id in trade_ids:
                self.close_trade(id)
