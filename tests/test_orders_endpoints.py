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
        """Testing invalid orders for raising all errors except HTTPError."""
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


if __name__ == "__main__":
    unittest.main()
