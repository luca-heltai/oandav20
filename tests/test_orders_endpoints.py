import unittest

from requests import HTTPError

from oandav20.testing import TestCase


class TestOrdersMethods(TestCase):
    """Tests for the OrdersMixin class."""

    def test_create_market_order(self):
        """Testing market order for the 'create_order' method."""
        response = self.oanda.create_order("MARKET", "AUD_USD", "BUY", 1)

        self.assertTrue(response)

    def test_create_limit_order(self):
        """Testing limit order for the 'create_order' method."""
        response = self.oanda.create_order("LIMIT", "AUD_USD", "SELL", 1,
                                           price=2.0, stoploss=2.1,
                                           takeprofit=1.9)
        self.assertTrue(response)

    def test_create_stop_order(self):
        """Testing stop order for the 'create_order' method."""
        with open("used_own_ids.txt") as f:
            last_id = f.read().split("\n")[-2]  # [-1] is blank string

        with open("used_own_ids.txt", "a") as f:
            f.write(str(int(last_id) + 1) + "\n")

        response = self.oanda.create_order("STOP", "AUD_USD", "BUY", 1,
                                           price=0.1, price_bound=0.1001,
                                           own_id="AUD_USD_" + last_id,
                                           tag="foo", comment="comment")

        self.assertTrue(response)

    def test_create_invalid_orders(self):
        """Testing invalid orders for raising all errors except HTTPError
        inside the 'create_order' method."""
        with self.assertRaises(ValueError):
            self.oanda.create_order("foo", "AUD_USD", "BUY", 1)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "foo", "BUY", 1)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "AUD_USD", "foo", 1)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "AUD_USD", "BUY", 0)

        with self.assertRaises(ValueError):
            self.oanda.create_order("MARKET", "AUD_USD", "BUY", 1,
                                    time_in_force="GTC")

        with self.assertRaises(TypeError):
            self.oanda.create_order("LIMIT", "AUD_USD", "BUY", 1)

    def test_get_order_by_oanda_id(self):
        """Testing getting single order details by Oanda ID in the 'get_order'
        method.

        The same behaviour would be for any method working with Oanda order /
        trade ID."""
        response = self.oanda.get_order(5)

        self.assertEqual(str(5), response["order"]["id"])

    def test_get_order_by_own_id(self):
        """Testing getting single order details by own ID in the 'get_order'
        method."""
        response = self.oanda.get_order(own_id="AUD_USD_1")

        self.assertEqual(
            "AUD_USD_1", response["order"]["clientExtensions"]["id"])

    def test_missing_argument_for_get_order(self):
        """Testing missing argument for 'order_id' and 'own_id' in the
        'get_order' method.

        The same behaviour would be for any method working with Oanda order /
        trade ID or own ID."""
        with self.assertRaises(TypeError):
            self.oanda.get_order()

    def test_get_filtered_orders(self):
        """Testing the 'get_filtered_orders' method."""
        self.oanda.create_order("LIMIT", "EUR_USD", "BUY", 1, price=0.1)
        self.oanda.create_order("STOP", "EUR_USD", "BUY", 1, price=2.0)
        response = self.oanda.get_filtered_orders("EUR_USD")

        self.assertEqual(2, len(response["orders"]))

    def test_get_all_orders(self):
        """Testing the 'get_all_orders' method."""
        response = self.oanda.get_all_orders()

        self.assertGreaterEqual(len(response["orders"]), 0)

    def test_update_order(self):
        """Testing the 'update_order' method."""
        order_id = self.oanda.create_order("LIMIT", "GBP_USD", "BUY", 1,
                                           price=0.1)
        response = self.oanda.update_order(order_id, price=0.11, stoploss=0.9,
                                           takeprofit=0.2, units=2)
        self.assertTrue(response)

    def test_update_order_extensions(self):
        """Testing the 'update_order_extensions' method."""
        with open("used_own_ids.txt") as f:
            last_id = f.read().split("\n")[-2]  # [-1] is blank string

        own_id = "GBP_USD_" + last_id
        self.oanda.create_order("STOP", "GBP_USD", "BUY", 1, price=2.0,
                                own_id=own_id)
        response = self.oanda.update_order_extensions(own_id=own_id, tag="foo",
                                                      comment="bar")

        self.assertTrue(response)

    def test_cancel_order(self):
        """Testing the 'cancel_order' method."""
        order_id = self.oanda.create_order("LIMIT", "NZD_USD", "BUY", 1, 0.1)
        response = self.oanda.cancel_order(order_id)

        self.assertTrue(response)

    def test_cancel_filtered_orders(self):
        """Testing the 'cancel_filtered_orders' method."""
        self.oanda.create_order("LIMIT", "USD_CAD", "SELL", 1, price=2.0)
        self.oanda.create_order("STOP", "USD_CAD", "BUY", 1, price=2.0)
        self.oanda.cancel_filtered_orders(instrument="USD")
        response = self.oanda.get_all_orders()

        self.assertFalse(response["orders"])

    def test_cancel_all_orders(self):
        """Testing the 'cancel_all_orders' method."""
        self.oanda.create_order("LIMIT", "USD_JPY", "BUY", 1, price=1.0)
        self.oanda.create_order("STOP", "USD_JPY", "SELL", 1, price=1.0)
        self.oanda.cancel_all_orders()
        response = self.oanda.get_all_orders()

        self.assertFalse(response["orders"])
        

if __name__ == "__main__":
    unittest.main()
