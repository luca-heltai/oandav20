import unittest

from oandav20.testing import TestCase


class TestOrderMixin(TestCase):
    """
    For creating orders should be used forex pairs written below:

    "EUR_AUD",
    "EUR_CAD",
    "EUR_CHF",
    "EUR_CZK",
    "EUR_DKK",
    "EUR_GBP",
    "EUR_HKD",
    "EUR_HUF",
    "EUR_JPY",
    "EUR_NOK",
    "EUR_NZD",
    "EUR_PLN",
    "EUR_SEK",
    "EUR_SGD",
    "EUR_TRY",
    "EUR_USD",
    "EUR_ZAR"
    """

    def tearDown(self):
        with open("used_own_ids.txt", "a") as f:
            f.write(str(int(self.last_own_id) + 1) + "\n")

    @property
    def last_own_id(self):
        with open("used_own_ids.txt") as f:
            last_own_id = f.read().split("\n")[-2]  # [-1] is blank string

        return last_own_id

    def test_create_order_method(self):
        # Market order

        order_id = self.oanda.create_order("MARKET", "EUR_AUD", "BUY", 1)
        assert type(int(order_id)) is int

        order_details = self.oanda.get_order(order_id)
        assert order_details["order"]["id"] == order_id

        # Limit order

        order_id = self.oanda.create_order(
            "LIMIT", "EUR_CAD", "BUY", 1, price=0.1, stoploss=2.1,
            takeprofit=1.9)
        assert type(int(order_id)) is int

        order_details = self.oanda.get_order(order_id)
        assert order_details["order"]["id"] == order_id

        # Stop order

        own_id = "EUR_CHF_" + self.last_own_id
        is_created = self.oanda.create_order(
            "STOP", "EUR_CHF", "SELL", 1, price=0.1, price_bound=0.0995,
            own_id=own_id, tag="foo", comment="bar")
        assert is_created

        order_details = self.oanda.get_order(own_id=own_id)
        assert order_details["order"]["clientExtensions"]["id"] == own_id

        # Now try invalid arguments

        with self.assertRaises(ValueError):
            self.oanda.create_order("foo", "EUR_CZK", "BUY", 1)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "foo", "BUY", 1)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "EUR_CZK", "foo", 1)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "EUR_CZK", "BUY", 0)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "EUR_CZK", "BUY", 1,
                                    time_in_force="GTC")

        with self.assertRaises(TypeError):
            self.oanda.create_order("LIMIT", "EUR_CZK", "BUY", 1)

    def test_create_market_order_method(self):
        order_id = self.oanda.create_market_order("EUR_DKK", "BUY", 1)
        assert order_id

    def test_create_limit_order_method(self):
        order_id = self.oanda.create_limit_order(
            "EUR_GBP", "BUY", 1, price=0.1)
        assert order_id

    def test_create_stop_order_method(self):
        order_id = self.oanda.create_stop_order(
            "EUR_HKD", "SELL", 1, price=0.1)
        assert order_id

    def test_get_order_method(self):
        """There are used old Oanda order ID and own order ID."""
        order_details = self.oanda.get_order(5)
        assert order_details["order"]["id"] == str(5)

        order_details = self.oanda.get_order(own_id="AUD_USD_1")
        assert order_details["order"]["clientExtensions"]["id"] == "AUD_USD_1"

        with self.assertRaises(TypeError):
            self.oanda.get_order()

    def test_get_all_orders_method(self):
        self.oanda.create_limit_order("EUR_HUF", "BUY", 1, price=0.1)

        pending_orders = self.oanda.get_all_orders()
        assert len(pending_orders["orders"]) >= 1

        pending_orders_instrument_list = \
            [order["instrument"] for order in pending_orders["orders"]]
        assert "EUR_HUF" in pending_orders_instrument_list

    def test_update_order_method(self):
        order_id = self.oanda.create_limit_order(
            "EUR_JPY", "BUY", 1, price=0.1)

        new_order_id = self.oanda.update_order(
            order_id, price=0.11, stoploss=0.9, takeprofit=0.2, units=2)
        assert new_order_id

        order_details = self.oanda.get_order(new_order_id)
        assert order_details["order"]["units"] == str(2)

    def test_update_order_extensions_method(self):
        own_id = "EUR_NOK_" + self.last_own_id
        self.oanda.create_limit_order(
            "EUR_NOK", "BUY", 1, price=0.1, own_id=own_id)

        is_updated = self.oanda.update_order_extensions(
            own_id=own_id, tag="foo", comment="bar")
        assert is_updated

        order_details = self.oanda.get_order(own_id=own_id)
        assert order_details["order"]["clientExtensions"]["id"] == own_id

    def test_cancel_order_method(self):
        order_id = self.oanda.create_limit_order("EUR_NZD", "BUY", 1, 0.1)

        is_canceled = self.oanda.cancel_order(order_id)
        assert is_canceled

        pending_orders = self.oanda.get_all_orders()
        pending_orders_instrument_list = \
            [order["instrument"] for order in pending_orders["orders"]]
        assert "EUR_NZD" not in pending_orders_instrument_list

    def test_cancel_filtered_orders_method(self):
        own_id_1 = "EUR_PLN_" + self.last_own_id
        self.oanda.create_market_order("EUR_PLN", "BUY", 1, own_id=own_id_1)

        own_id_2 = "EUR_SEK_" + self.last_own_id
        self.oanda.create_market_order("EUR_SEK", "BUY", 1, own_id=own_id_2)

        self.oanda.cancel_filtered_orders(own_ids=[own_id_1, own_id_2])

        pending_orders = self.oanda.get_all_orders()
        pending_orders_own_ids_list = \
            [order["clientExtensions"]["id"] for order in \
             pending_orders["orders"]]
        assert own_id_1 not in pending_orders_own_ids_list
        assert own_id_2 not in pending_orders_own_ids_list

        self.oanda.cancel_filtered_orders(instrument="EUR")

        pending_orders = self.oanda.get_all_orders()
        assert not len(pending_orders["orders"])

    def test_cancel_all_orders_method(self):
        self.oanda.create_limit_order("EUR_SGD", "BUY", 1, price=0.1)
        self.oanda.cancel_all_orders()
        
        pending_orders = self.oanda.get_all_orders()
        assert not len(pending_orders["orders"])


if __name__ == "__main__":
    unittest.main()
