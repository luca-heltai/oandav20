class TradesMixin:
    """Methods in the TradesMixin class handles the trades endpoints."""

    def get_open_trades(self, account_id=""):
        """Get list of all open trades.

        Arguments:
            account_id (str, optional):
                Oanda account ID.

        Returns:
            JSON object with the open trades details.

        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/openTrades".format(account_id)

        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_trade_details(self, trade_id=0, own_id="", account_id=""):
        """Get details for the given trade.

        Arguments:
            trade_id (int, optional):
                Trade ID provided by Oanda.
            own_id (str, optinal):
                Custom trade ID.
            account_id (str, optional):
                Oanda account ID

        Returns:
            JSON object with the trade details.

        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'trade_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not trade_id and not own_id:
            raise TypeError("Missing argument either for the 'trade_id' or "
                            "'own_id' parameter.")

        if own_id:
            trade_id = "@" + own_id

        endpoint = "/{0}/trades/{1}".format(account_id, trade_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def update_trade(self, trade_id=0, own_id="", stoploss=0.0,
                     trailing_stoploss=0.0, takeprofit=0.0, account_id=""):
        """Create / update / remove values for the given order, eg. stoploss.

        User may choose if wants to update the trade by Oanda ID or custom ID.

        Note:
            For removing / erasing values pass negative float number.

        Arguments:
            trade_id (int, optional):
                Trade ID provided by Oanda.
            own_id (str, optional):
                Custom trade ID.
            stoploss (float, optinal):
                Stoploss in the price format.
            trailing_stoploss (float, optinal):
                Trailing stoploss in the price format.
            takeprofit (float, optinal):
                Takeprofit in the price format.
            account_id (str, optional):
                Oanda account ID.

        Returns:
            True, if the trade update was succesful.

        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'trade_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not trade_id and not own_id:
            raise TypeError("Missing argument either for the 'trade_id' or "
                            "'own_id' parameter.")

        if own_id:
            trade_id = "@" + own_id

        endpoint = "/{0}/orders/{1}".format(account_id, trade_id)

        # In this method is different trade structure unlike order in the
        # OrdersMixin clas.

        body = {}

        if stoploss:
            if stoploss < 0:
                stoploss = 0

            body["stopLoss"] = {
                "price": str(stoploss),
                "timeInForce": "GTC"
            }

        if trailing_stoploss:
            if trailing_stoploss < 0:
                trailing_stoploss = 0

            body["trailingStoploss"] = {
                "distance": str(trailing_stoploss),
                "timeInForce": "GTC"
            }

        if takeprofit:
            if takeprofit < 0:
                takeprofit = 0

            body["takeProfit"] = {
                "price": str(takeprofit),
                "timeInForce": "GTC"
            }

        response = self.send_request(endpoint, "PUT", json=body)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 201

    def update_trade_extensions(self):
        pass

    def close_trade(self, trade_id=0, own_id="", units=0, account_id=""):
        """Close fully or partially the given open trade.

        User may choose if wants to close the trade by Oanda ID or custom ID.

        Arguments:
            trade_id (int, optional):
                Trade ID provided by Oanda.
            own_id (str, optional):
                Custom trade ID.
            units (int, optional):
                How many units should be closed. If empty then all units will
                be used.
            account_id (str, optional):
                Oanda account ID.

        Returns:
            True if the trade was closed properly.

        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'trade_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not trade_id and not own_id:
            raise TypeError("Missing argument either for the 'trade_id' or "
                            "'own_id' parameter.")

        if own_id:
            trade_id = "@" + own_id

        endpoint = "/{0}/trades/{1}/close".format(account_id, trade_id)

        if units:
            body = {"units": str(units)}
            response = self.send_request(endpoint, "PUT", json=body)
        else:
            response = self.send_request(endpoint, "PUT")

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 200
