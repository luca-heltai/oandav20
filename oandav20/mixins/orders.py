from typing import Any, List, Union

from .account import INSTRUMENTS


class OrdersMixin:
    """Methods in the OrdersMixin class handles the orders endpoints."""

    def create_order(self, order_type: str, instrument: str, side: str,
                     units: int, price: float = 0.0, price_bound: float = 0.0,
                     time_in_force: str = "", stoploss: float = 0.0,
                     takeprofit: float = 0.0, own_id: str = "", tag: str = "",
                     comment: str = "", account_id: str = "") \
            -> Union[bool, str]:
        """Create an order for the given instrument with specified parameters.

        If a user didn't place own ID then he / she must remember order ID
        created by Oanda and himself / herself check if the order is still
        pending or filled.

        Therefore I highly recommend to use own ID, for example "EUR_USD_1"
        which be used both for orders and trades.

        Arguments:
            order_type:
                Type of order, accepting only value "MARKET", "LIMIT" or
                "STOP".
            instrument:
                Code of instrument.
            side:
                Side of order, accepting only value "BUY" or "SELL".
            units:
                Size of order.
            price:
                Price level for orders "LIMIT" and "STOP".
            price_bound:
                The worse market price that may be filled, goes only for "STOP"
                order.
            time_in_force:
                How long should the order remain pending. Accepting only codes
                "FOK" or "IOC" for the "MARKET" order, for the rest "GTC" or
                "GFD" codes. "FOK" is default for the "MARKET" type and "GTC"
                for the waiting types.
            stoploss:
                Stoploss level.
            takeprofit:
                Takeprofit level.
            own_id:
                Own ID used for this order and if filled, then also for
                the open trade.
            tag:
                User tag.
            comment:
                User comment.
            account_id:
                Oanda trading account ID.

        Returns:
            True if the order was created as specified and user used own ID or
            returns order ID created by Oanda.

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Argument for the 'price' parameter is required, if the order
                type is either "LIMIT" or "STOP".
            ValueError:
                1. Invalid order type passed to the 'order_type' parameter.
                2. Invalid instrument code passed to the 'instrument'
                    parameter.
                3. Invalid side passes to the 'side' parameter.
                4. Invalid size of units passed to the 'units' parameter.
                5. Invalid TimeInForce code for the given order type passed
                    to the 'time_in_force' parameter.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/orders".format(account_id)

        if order_type not in ["MARKET", "LIMIT", "STOP"]:
            raise ValueError("Invalid order type '{}'.".format(order_type))

        if instrument not in INSTRUMENTS.values():
            raise ValueError("Invalid instrument code '{}'.".format(
                instrument))

        if side not in ["BUY", "SELL"]:
            raise ValueError("Invalid side '{}'.".format(side))

        if not units > 0:
            raise ValueError("Invalid size of units '{}'.".format(units))

        # Units must be negative for the "SELL" order.

        if side == "SELL":
            units = units * -1

        if order_type == "MARKET":
            if time_in_force:
                if time_in_force in ["FOK", "IOC"]:
                    time_in_force = time_in_force
                else:
                    raise ValueError("Invalid TimeInForce code '{}' for the "
                                     "'{}' order.".format(
                                         time_in_force, order_type))
            else:
                time_in_force = "FOK"
        elif order_type in ["LIMIT", "STOP"]:
            if time_in_force:
                if time_in_force in ["GTC", "GFD"]:
                    time_in_force = time_in_force
                else:
                    raise ValueError("Invalid TimeInForce code '{}' for the "
                                     "'{}' order.".format(
                                         time_in_force, order_type))
            else:
                time_in_force = "GTC"

            # Argument for the 'price' parameter is required for these order
            # types.

            if not price:
                raise TypeError("Missing argument for the 'price' parameter "
                                "in the '{}' order".format(order_type))

        request_body = {
            "order": {
                "instrument": instrument,
                "positionFill": "DEFAULT",
                "timeInForce": time_in_force,
                "type": order_type,
                "units": str(units),

                # Voluntary keys (if empty, Oanda will ignore that)-

                "clientExtensions": {
                    "comment": comment,
                    "id": str(own_id),
                    "tag": tag
                },
                "tradeClientExtensions": {
                    "comment": comment,
                    "id": str(own_id),
                    "tag": tag
                }
            }
        }

        # Other voluntary keys which cannot be placed in the 'request_body'
        # variable if they are empty, otherwise Oanda raises error messages
        # for them.

        if price and order_type in ["LIMIT", "STOP"]:
            request_body["order"]["price"] = str(price)

        if price_bound and order_type in ["MARKET", "STOP"]:
            request_body["order"]["priceBound"] = str(price_bound)

        if stoploss:
            request_body["order"]["stopLossOnFill"] = {
                "price": str(stoploss),
                "timeInForce": "GTC"
            }

        if takeprofit:
            request_body["order"]["takeProfitOnFill"] = {
                "price": str(takeprofit),
                "timeInForce": "GTC"
            }

        response = self.send_request(endpoint, "POST", json=request_body)

        if response.status_code >= 400:
            response.raise_for_status()

        if not own_id:
            return response.json()["orderCreateTransaction"]["id"]
        else:
            return response.status_code == 201

    def create_market_order(self, *args: Any, **kwargs: Any) \
            -> Union[bool, str]:
        """Alias for the 'create_order' with first argument "MARKET".

        Arguments:
            args:
                Same args like for the 'create_order'
            kwargs:
                Same kwargs like for the 'create_order'

        Returns:
            Call the 'create_order' method with first argument "MARKET".
        """
        return self.create_order("MARKET", *args, **kwargs)

    def create_limit_order(self, *args: Any, **kwargs: Any) \
            -> Union[bool, str]:
        """Alias for the 'create_order' with first argument "LIMIT".

        Arguments:
            args:
                Same args like for the 'create_order'
            kwargs:
                Same kwargs like for the 'create_order'

        Returns:
            Call the 'create_order' method with first argument "LIMIT".
        """
        return self.create_order("LIMIT", *args, **kwargs)

    def create_stop_order(self, *args: Any, **kwargs: Any) \
            -> Union[bool, str]:
        """Alias for the 'create_order' with first argument "STOP".

        Arguments:
            args:
                Same args like for the 'create_order'
            kwargs:
                Same kwargs like for the 'create_order'

        Returns:
            Call the 'create_order' method with first argument "STOP".
        """
        return self.create_order("STOP", *args, **kwargs)

    def get_order(self, order_id: int = 0, own_id: str = "",
                  account_id: str = "") \
            -> dict:
        """Get details for the given order ID.

        User may choose if the order details will be obtained by Oanda ID or
        its ID.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Own ID.
            account_id:
                Oanda trading account ID.

        Returns:
            JSON object (dict) with the order details.

        Example:
            {
                "lastTransactionID": "6375",
                "order": {
                    "clientExtensions": {
                        "comment": "New idea for trading",
                        "id": "my_order_100",
                        "tag": "strategy_9"
                    },
                    "createTime": "2016-06-22T18:41:29.294265338Z",
                    "id": "6375",
                    "instrument": "EUR_CAD",
                    "partialFill": "DEFAULT_FILL",
                    "positionFill": "POSITION_DEFAULT",
                    "price": "1.30000",
                    "replacesOrderID": "6373",
                    "state": "PENDING",
                    "timeInForce": "GTC",
                    "triggerCondition": "TRIGGER_DEFAULT",
                    "type": "STOP",
                    "units": "10000"
                }
            }

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'order_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not order_id and not own_id:
            raise TypeError("Missing argument either for the 'order_id' or "
                            "'own_id'.")

        if own_id:
            own_id = "@" + own_id

        used_id = order_id or own_id
        endpoint = "/{0}/orders/{1}".format(account_id, used_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_all_orders(self, account_id: str = "") -> dict:
        """Get list of all pending orders.

        Arguments:
            account_id:
                Oanda trading account ID.

        Returns:
            JSON object (dict) with the pending orders details.

        Example:
            {
                "lastTransactionID": "6375",
                "orders": [
                    {
                        "clientExtensions": {
                            "comment": "New idea for trading",
                            "id": "my_order_100",
                            "tag": "strategy_9"
                        },
                        "createTime": "2016-06-22T18:41:29.294265338Z",
                        "id": "6375",
                        "instrument": "EUR_CAD",
                        "partialFill": "DEFAULT_FILL",
                        "positionFill": "POSITION_DEFAULT",
                        "price": "1.30000",
                        "replacesOrderID": "6373",
                        "state": "PENDING",
                        "timeInForce": "GTC",
                        "triggerCondition": "TRIGGER_DEFAULT",
                        "type": "STOP",
                        "units": "10000"
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
        endpoint = "/{}/pendingOrders".format(account_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def update_order(self, order_id: int = 0, own_id: str = "",
                     price: float = 0.0, price_bound: float = 0.0,
                     stoploss: float = 0.0, takeprofit: float = 0.0,
                     units: int = 0, account_id: str = "") \
            -> Union[bool, str]:
        """Update values for the specific pending order.

        User may update only values such as 'price', 'stoploss', 'takeprofit'
        etc., not change instrument or even order type / side. For these
        situations must close the pending order himself / herself and create
        new one.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Own ID.
            price:
                Price level for waiting orders.
            price_bound:
                The worse market price that may be filled, goes only for "STOP"
                order.
            stoploss:
                Stoploss level.
            takeprofit:
                Maximal profit.
            units:
                Order size.
            account_id:
                Oanda trading account ID.

        Returns:
            True if used own ID or new Oanda order ID if the old Oanda order
            ID was used.

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'order_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not order_id and not own_id:
            raise TypeError("Missing argument either for the 'order_id' or "
                            "'own_id'.")

        if order_id:
            used_oanda_id = True
            old_order_details = self.get_order(
                order_id, account_id=account_id)["order"]

        if own_id:
            own_id = "@" + own_id
            old_order_details = self.get_order(
                own_id=own_id, account_id=account_id)["order"]

        used_id = order_id or own_id
        endpoint = "/{0}/orders/{1}".format(account_id, used_id)

        # Oanda added internal keys which are incompatible with the order
        # structure within request body.

        unwanted_keys = [
            "createTime", "id", "partialFill", "state", "triggerCondition"
        ]

        for key in unwanted_keys:
            old_order_details.pop(key)

        # Change value for key "positionFill" to "DEFAULT" because Oanda
        # has changed internally the value for their purposes and is also
        # incompatible ...

        old_order_details["positionFill"] = "DEFAULT"

        if price:
            old_order_details["price"] = str(price)

        if price_bound and old_order_details["order"]["type"] == "STOP":
            old_order_details["priceBound"] = str(price_bound)

        if stoploss:
            try:
                old_order_details["stopLossOnFill"]["price"] = str(stoploss)
            except KeyError:
                old_order_details["stopLossOnFill"] = {
                    "price": str(stoploss),
                    "timeInForce": "GTC"
                }

        if takeprofit:
            try:
                old_order_details["takeProfitOnFill"]["price"] = \
                    str(takeprofit)
            except KeyError:
                old_order_details["takeProfitOnFill"] = {
                    "price": str(takeprofit),
                    "timeInForce": "GTC"
                }

        if units > 0:
            old_order_details["units"] = str(units)

        new_order = {"order": old_order_details}
        response = self.send_request(endpoint, "PUT", json=new_order)

        if response.status_code >= 400:
            response.raise_for_status()

        if used_oanda_id:
            return response.json()["orderCreateTransaction"]["id"]
        else:
            return response.status_code == 201

    def update_order_extensions(self, order_id: int = 0, own_id: str = "",
                                new_own_id: str = "", tag: str = "",
                                comment: str = "", account_id: str = "") \
            -> bool:
        """Update client extensions for the given order.

        User may choose if wants to get the order by Oanda ID or its ID.

        Note:
            New own ID or tag should be used very rarely in my opinion.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Own ID.
            new_own_id:
                New own ID which will replace existing own ID.
            tag:
                New tag.
            comment:
                New comment.
            account_id:
                Oanda trading account ID.

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

        if not order_id and not own_id:
            raise TypeError("Missing argument either for the 'order_id' or "
                            "'own_id'.")

        if own_id:
            own_id = "@" + own_id

        used_id = order_id or own_id
        endpoint = \
            "/{0}/orders/{1}/clientExtensions".format(account_id, used_id)
        request_body = {
            "clientExtensions": {},
            "tradeClientExtensions": {}
        }

        if new_own_id:
            request_body["clientExtensions"]["id"] = new_own_id
            request_body["tradeClientExtensions"]["id"] = new_own_id

        if tag:
            request_body["clientExtensions"]["tag"] = tag
            request_body["tradeClientExtensions"]["tag"] = tag

        if comment:
            request_body["clientExtensions"]["comment"] = comment
            request_body["tradeClientExtensions"]["comment"] = comment

        response = self.send_request(endpoint, "PUT", json=request_body)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 200

    def cancel_order(self, order_id: int = 0, own_id: str = "",
                     account_id="") \
            -> bool:
        """Cancel the given pending order.

        User may choose if the order details will be obtained by Oanda ID or
        its ID.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Own ID.
            account_id:
                Oanda trading account ID.

        Returns:
            True, if the pending order was cancelled.

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'order_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not order_id and not own_id:
            raise TypeError("Missing argument either for the 'order_id' or "
                            "'own_id'.")

        if own_id:
            own_id = "@" + own_id

        used_id = order_id or own_id
        endpoint = "/{0}/orders/{1}/cancel".format(account_id, used_id)
        response = self.send_request(endpoint, "PUT")

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 200

    def cancel_filtered_orders(self, order_ids: List[int] = [],
                               own_ids: List[str] = [], instrument: str = "",
                               account_id: str = "") \
            -> None:
        """Cancel the filtered pending orders if there are any.

        This method is very useful for situations where is important to
        cancel all pending orders which relate to USD currency before news are
        released.

        Arguments:
            order_ids:
                Order IDs provided by Oanda.
            own_ids:
                Own orders IDs (via 'own_id').
            instrument:
                Instrument code or also single currency code.

        Raises:
            TypeError:
                Missing argument either for the 'order_ids' or 'own_ids' or
                'instrument' parameter.

        Todo:
            - refactor to async
        """
        account_id = account_id or self.default_id

        if not order_ids and not own_ids and not instrument:
            raise TypeError("Missing argument either for the 'order_ids' or "
                            "'own_ids' or 'instrument'.")

        pending_orders = self.get_all_orders(account_id)

        if pending_orders["orders"]:
            if order_ids:
                for id in order_ids:
                    self.cancel_order(id, account_id=account_id)

                return

            if own_ids:
                for id in own_ids:
                    self.cancel_order(own_id=id, account_id=account_id)

                return

            if instrument:
                orders_dict = \
                    {int(order["id"]): order["instrument"] for order in
                     pending_orders["orders"]}

                for key, value in orders_dict.items():
                    if instrument in orders_dict[key]:
                        self.cancel_order(key, account_id=account_id)

                return

    def cancel_all_orders(self, account_id: str = "") -> None:
        """Cancel all pending orders if there are any.

        Arguments:
            account_id:
                Oanda trading account ID.

        Todo:
            - refactor to async
        """
        account_id = account_id or self.default_id
        pending_orders = self.get_all_orders(account_id)

        if pending_orders["orders"]:
            orders_ids = \
                [int(order["id"]) for order in pending_orders["orders"]]

            for id in orders_ids:
                self.cancel_order(id, account_id=account_id)
