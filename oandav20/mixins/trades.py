from typing import List

from oandav20.mixins.account import INSTRUMENTS


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
        """Update editable values (see the parameters) for the given order.

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
        endpoint = "/{0}/trades/{1}/orders".format(account_id, used_id)
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

        return response.status_code == 200

    def update_trade_extensions(self, trade_id: int = 0, own_id: str = "",
                                tag: str = "", comment: str = "",
                                account_id: str = "") \
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

        if not trade_ids and not own_ids and not instrument:
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
