from typing import List, Union

from .account import INSTRUMENTS

ORDER_TYPE = ["MARKET", "LIMIT", "STOP", "MARKET_IF_TOUCHED"]
SIDE = ["BUY", "SELL"]
TIME_IN_FORCE = ["FOK", "IOC", "GTC", "GTD", "GFD"]


class OrdersMixin:
    """Methods in the OrdersMixin class handles the orders endpoints."""

    def create_order(self, order_type: str, instrument: str, side: str,
                     units: int, price: float = 0.0, price_bound: float = 0.0,
                     time_in_force: str = "", gtd_time: str = "",
                     stoploss: float = 0.0, trailing_stoploss: float = 0.0,
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
                Type of order, accepting only value "MARKET", "LIMIT", "STOP"
                or "MARKET_IF_TOUCHED".
            instrument:
                Code of instrument.
            side:
                Side of order, accepting only value "BUY" or "SELL".
            units:
                Size of order.
            price:
                Price level for orders "LIMIT", "STOP" and "MARKET_IF_TOUCHED".
            price_bound:
                The worse market price that may be filled, goes only for orders
                "STOP" and "MARKET_IF_TOUCHED".
            time_in_force:
                How long should the order remain pending. Accepting only codes
                "FOK" or "IOC" for the "MARKET" order, for the rest "GTC" or
                "GTD" or "GFD" codes. "FOK" is default for the "MARKET" type
                and "GTC" for the waiting types.
            gtd_time:
                String represention of DateTime object in RFC 3339 format for
                orders with value "GTD" in the 'time_in_force'.
            stoploss:
                Stoploss level.
            trailing_stoploss:
                Trailing stopllos level, Oanda itself calculcate the
                difference in pips between this trailing stoploss level and
                triggered price.
            takeprofit:
                Takeprofit level.
            own_id:
                Custom user ID used for this order and if filled, then also for
                the open trade.
            tag:
                Custom user tag.
            comment:
                Custom user comment.
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
                type is either "LIMIT" or "STOP" or "MARKET_IF_TOUCHED".
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

        if order_type not in ORDER_TYPE:
            raise ValueError("Invalid order type '{}'.".format(order_type))

        if instrument not in INSTRUMENTS.values():
            raise ValueError("Invalid instrument code '{}'.".format(
                instrument))

        if side not in SIDE:
            raise ValueError("Invalid side '{}'.".format(side))

        if not units > 0:
            raise ValueError("Invalid size of units '{}'.".format(units))

        # Units have to be negative for the "SELL" order.

        if side == "SELL":
            units = units * -1

        if order_type == "MARKET":
            if time_in_force:
                if time_in_force in TIME_IN_FORCE[:2]:
                    time_in_force = time_in_force
                else:
                    raise ValueError("Invalid TimeInForce code '{}' for the "
                                     "'{}' order.".format(
                                        time_in_force, order_type))
            else:
                time_in_force = "FOK"
        elif order_type in ORDER_TYPE[1:]:
            if time_in_force:
                if time_in_force in TIME_IN_FORCE[2:]:
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
                # Mandatory keys for all order types.

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
                }
            }
        }

        # Other voluntary keys which cannot be placed in the 'request_body'
        # variable if they are empty, otherwise Oanda raises error messages
        # for them.

        if gtd_time and time_in_force == "GTD":
            request_body["order"]["gtdTime"] = gtd_time

        if price:
            request_body["order"]["price"] = str(price)

        if price_bound:
            request_body["order"]["priceBound"] = str(price_bound)

        if stoploss:
            request_body["order"]["stopLossOnFill"] = {
                "price": str(stoploss),
                "timeInForce": "GTC"
            }

        if trailing_stoploss:
            request_body["order"]["trailingStopLossOnFill"] = {
                "distance": str(trailing_stoploss),
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

    def get_order(self, order_id: int = 0, own_id: str = "",
                  account_id: str = "") \
            -> dict:
        """Get details for the given order ID.

        User may choose if the order details will be obtained by Oanda ID or
        custom ID.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Custom ID.
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
                    "type": "MARKET_IF_TOUCHED",
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

    def get_filtered_orders(self, order_ids: List[int] = [],
                            instrument: str = "", account_id: str = "") \
            -> dict:
        """Get list of filtered pending orders.

        There are picked only the two filters (see parameters) which I
        consider as reasonable.

        Arguments:
            order_ids:
                List of Oanda order IDs, not custom order IDs.
            instrument:
                Code of single instrument.
            account_id:
                Oanda trading account ID.

        Returns:
            JSON object (dict) with the filtered pending orders details.

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
                        "type": "MARKET_IF_TOUCHED",
                        "units": "10000"
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
        endpoint = "/{}/orders".format(account_id)
        url_params = {}

        if order_ids:
            joined_ids = ",".join([str(id) for id in order_ids])
            url_params["ids"] = joined_ids

        if instrument:
            if instrument in INSTRUMENTS:
                url_params["instrument"] = instrument
            else:
                raise ValueError("Invalid instrument code {}.".format(
                    instrument))

        response = self.send_request(endpoint, params=url_params)

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
                        "type": "MARKET_IF_TOUCHED",
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
                     stoploss: float = 0.0, trailing_stoploss: float = 0.0,
                     takeprofit: float = 0.0, units: int = 0,
                     account_id: str = "") \
            -> Union[bool, str]:
        """Update values for the specific pending order.

        User may update only such as values 'price', 'stoploss', 'takeprofit'
        etc., not change instrument or even order type / side. For these
        situations must close the pending order himself / herself and create
        new one.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Custom ID.
            price:
                Price level for waiting orders.
            price_bound:
                The worse market price that may be filled, goes only for order
                "MARKET_IF_TOUCHED".
            stopLoss:
                Stoploss level.
            trailing_stoploss:
                Trailing stopllos level, Oanda itself calculcate the
                difference in pips between this trailing stoploss level and
                triggered price.
            takeprofit:
                Maximal profit.
            units:
                Order size.
            account_id:
                Oanda trading account ID.

        Returns:
            True if used custom ID or new Oanda order ID if the old Oanda order
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
            old_order_details = self.get_order_details(
                order_id, account_id=account_id)["order"]

        if own_id:
            own_id = "@" + own_id
            old_order_details = self.get_order_details(
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

        if price_bound and old_order_details["order"]["type"] == \
                "MARKET_IF_TOUCHED":
            old_order_details["priceBound"] = str(price_bound)

        if stoploss:
            try:
                old_order_details["stopLossOnFill"]["price"] = str(stoploss)
            except KeyError:
                old_order_details["stopLossOnFill"] = {
                    "price": str(stoploss),
                    "timeInForce": "GTC"
                }

        if trailing_stoploss:
            try:
                old_order_details["trailingStopLossOnFill"]["distance"] = \
                    str(trailing_stoploss)
            except KeyError:
                old_order_details["trailingStopLossOnFill"] = {
                    "distance": str(trailing_stoploss),
                    "timeInForce": "GTC"
                }

        if takeprofit:
            try:
                old_order_details["takeProfitOnFill"]["price"] = str(stoploss)
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

        User may choose if wants to get the order by Oanda ID or custom ID.

        Note:
            New custom ID or tag should be used very rarely in my opinion.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Custom ID.
            new_own_id:
                New custom ID which will replace existing custom ID.
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
        endpoint = "/{0}/orders/{1}/clientExtensions".format(
            account_id, used_id)
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

    def cancel_order(self, order_id: int = 0, own_id: str = "",
                     account_id="") \
            -> bool:
        """Cancel the given pending order.

        User may choose if the order details will be obtained by Oanda ID or
        custom ID.

        Arguments:
            order_id:
                Order ID provided by Oanda.
            own_id:
                Custom ID.
            account_id:
                Oanda trading account ID.

        Returns:
            True, if the pending order was cancelled.

        Raises:
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

    def cancel_all_orders(self):
        """Cancel all pending orders.

        Todo:
            - use async
        """
        pass
