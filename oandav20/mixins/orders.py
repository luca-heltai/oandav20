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

        If a used didn'ŧ place own ID then he / she must remember ID created by
        Oanda. Both IDs are necessary for futher manipulation with orders /
        trades.

        Arguments:
            order_type (str):
                Type of order, accepting only value "MARKET", "LIMIT", "STOP"
                or "MARKET_IF_TOUCHED".
            instrument (str):
                Code of instrument.
            side (str):
                Side of order, accepting only value "BUY" or "SELL".
            units (int):
                Quantity of order.
            price (float, optional):
                Price level for orders "LIMIT", "STOP" and "MARKET_IF_TOUCHED".
            price_bound (float, optional):
                The worse market price that may be filled, goes only for orders
                "STOP" and "MARKET_IF_TOUCHED".
            time_in_force (str, optional):
                How long should the order remain pending. Accepting only codes
                "FOK" or "IOC" for the "MARKET" order, for the rest "GTC" or
                "GTD" or "GFD" codes. "FOK" is default for the "MARKET" type
                and "GTC" for the waiting types.
            gtd_time (str, optional):
                String represention of DateTime object in RFC 3339 format.
            stoploss (int, optional):
                Price where the trade ends around and user losses money.
            trailing_stoploss (int, optional):
                Distance in price units from the triggered price of this order.
                In the other words, Oanda itself calculcate the difference in
                pips.
            takeprofit (int, optional):
                Price where the trade ends and user gets profit.
            own_id (str, optional):
                Custom user ID used for this order and if filled, then also for
                the open trade.
            tag (str, optional):
                Custom user tag for tagging this order.
            comment (str, optional):
                Custom user comment for this order.

        Returns:
            True if the order was created as specified and user used own ID or
            returns order ID created by Oanda.

        Raises:
            HttpError:
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
                5. Invalid TimeInForce code for the given type of order.

        Todo:
            - add 'position_fill' parameter if some day a user of this package
            will want use this option.
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

            # Argument for the "price" parameter is required for these order
            # types.

            if not price:
                raise TypeError("Missing argument for the 'price' parameter "
                                "in the '{}' order".format(order_type))

        # Content for the POST HTTP method.

        body = {
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

        # Other voluntary keys which cannot be placed in the "body" variable
        # if they are empty, otherwise Oanda raises error messages for them.

        if gtd_time and time_in_force == "GTD":
            body["order"].update({"gtdTime": gtd_time})

        if price:
            body["order"].update({"price": str(price)})

        if price_bound:
            body["order"].update({"priceBound": str(price_bound)})

        if stoploss:
            body["order"].update({
                "stopLossOnFill": {
                    "price": str(stoploss),
                    "timeInForce": "GTC"
                }
            })

        if trailing_stoploss:
            body["order"].update({
                "trailingStopLossOnFill": {
                    "distance": str(trailing_stoploss),
                    "timeInForce": "GTC"
                }
            })

        if takeprofit:
            body["order"].update({
                "takeProfitOnFill": {
                    "price": str(takeprofit),
                    "timeInForce": "GTC"
                }
            })

        response = self.send_request(endpoint, "POST", json=body)

        if response.status_code >= 400:
            response.raise_for_status()

        # ADD RETURNED OANDA ID IF USER DIDN'T SPECIFIED THE 'OWN_ID'.

        return response.status_code == 201

    def get_order(self, order_id: int = 0, own_id: str = "",
                  account_id: str = "") -> dict:
        """Get details for the given order ID.

        User may choose if the order details will be obtained by Oanda ID or
        custom ID.

        Arguments:
            order_id (int, optinal):
                Order ID provided by Oanda.
            own_id (str, optinal):
                Custom user ID used for identifying orders.
            account_id (str, optinal):
                Oanda account ID.

        Returns:
            JSON object (dict) with the order details.

        Raises:
            TypeError:
                Missing argument either for the 'order_id' or 'own_id'
                parameter.
        """
        account_id = account_id or self.default_id

        if not order_id and not own_id:
            raise TypeError("Missing argument either for the 'order_id' or "
                            "'own_id' parameter.")

        if own_id:
            own_id = "@" + own_id

        used_id = order_id or own_id
        endpoint = "/{0}/orders/{1}".format(account_id, used_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_filtered_orders(self, order_ids: List[int] = [], instrument: str
                            = "", account_id: str = "") -> dict:
        """Get list of filtered pending orders.

        There are picked only the two filters which I consider as reasonable.

        Arguments:
            order_ids (list of ints, optinal):
                List of Oanda order IDs, not custom order IDs.
            instrument (str, optional):
                Code of single instrument.
            account_id (str, optinal):
                Oanda account ID.

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
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            ValueError:
                Invalid instrument code passed to the 'instrument' parameter.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/orders".format(account_id)
        params = {}

        if order_ids:
            string_ids = [str(id) for id in order_ids]
            joined_ids = ",".join(string_ids)
            params["ids"] = joined_ids

        if instrument:
            if instrument in INSTRUMENTS:
                params["instrument"] = instrument
            else:
                raise ValueError("Invalid instrument code {}.".format(
                    instrument))

        response = self.send_request(endpoint, params=params)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_orders(self, account_id: str = "") -> dict:
        """Get list of all pending orders.

        Arguments:
            account_id (str, optinal):
                Oanda account ID.

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
                     account_id: str = "") -> Union[bool, str]:
        """Update values for the specific pending order.

        User may update only such as values 'price', 'stoploss', 'takeprofit'
        etc., not change change instrument or even order type / side. For these
        situations must close the pending order himself / herself and create
        new one.

        Arguments:
            order_id (int, optional):
                Oanda intern order ID.
            own_id (str, optional):
                Custom user order ID.
            price (float, optinal):
                Price for waiting orders.
            price_bound (float, optinal):
                The worst filled price.
            stopLoss (float, optinal):
                Maximal loss.
            trailing_stoploss (float, optinal):
                Moving maximal loss.
            takeprofit (float, optional):
                Maximal profit.
            units (int, optinal):
                Order size.
            account_id (str, optinal):
                Oanda account ID.

        Returns:
            True if used custom user ID or new Oanda order ID in string if the
            old Oanda order ID was used.

        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument either for the 'order_id' or 'own_id'
                parameter.

        Todo:
            - add more options for modyfying values, eg. 'gtd_time',
            'time_in_force' etc. if somebody wants that.
        """
        account_id = account_id or self.default_id

        if not order_id and not own_id:
            raise TypeError("Missing argument either for the 'order_id' or "
                            "'own_id' parameter.")

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
        # structure.

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

        if price_bound:
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

        if units:
            old_order_details["units"] = str(units)

        new_order = {"order": old_order_details}
        response = self.send_request(endpoint, "PUT", json=new_order)

        if response.status_code >= 400:
            response.raise_for_status()

        if used_oanda_id:
            return response.json()["orderCreateTransaction"]["id"]
        else:
            return True

    def update_order_extensions(self, order_id: int = 0, own_id: str = "",
                                new_own_id: str = "", tag: str = "",
                                comment: str = "", account_id: str = "") \
            -> bool:
        """Update client extensions for the given order.

        User may choose if wants to get the order by Oanda ID or custom ID.

        Note:
            New custom ID or tag should be used very rarely in my opinion.

        Arguments:
            order_id (int, optional):
                Trade ID provided by Oanda.
            own_id (str, optinal):
                User custom trade ID.
            new_own_id (str, optinal):
                New custom ID which will replace existing custom ID.
            tag (str, optinal):
                Trade tag.
            comment (str, optinal):
                Trade comment.

        Returns:
            True, if the trade was succesfully updated.

        Raises:
            HTTPError:
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
        http_body = {"clientExtensions": {}}

        if new_own_id:
            http_body["clientExtensions"]["id"] = new_own_id

        if tag:
            http_body["clientExtensions"]["tag"] = tag

        if comment:
            http_body["clientExtensions"]["comment"] = comment

        response = self.send_request(endpoint, "PUT", json=http_body)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 200

    def cancel_order(self, order_id: int = 0, own_id: str = "",
                     account_id="") -> bool:
        """Cancel pending order for the given order ID.

        User may choose if the order details will be obtained by Oanda ID or
        custom ID.

        Arguments:
            order_id (int, optinal):
                Order ID provided by Oanda.
            own_id (str, optinal):
                Custom user ID used for identifying orders.
            account_id (str, optinal):
                Oanda account ID.

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

    def cancel_orders(self):
        """Cancel all pending orders.

        Todo:
            - use async
        """
        pass
