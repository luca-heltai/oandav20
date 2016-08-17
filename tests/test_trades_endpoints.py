import unittest

from oandav20.testing import TestCase


class TestTradesMixin(TestCase):
    """
    For creating market orders should be used forex pairs written below:

    "USD_CAD",
    "USD_CHF",
    "USD_CNH",
    "USD_CZK",
    "USD_DKK",
    "USD_HKD",
    "USD_HUF",
    "USD_INR",
    "USD_JPY",
    "USD_MXN",
    "USD_NOK",
    "USD_PLN",
    "USD_SAR",
    "USD_SEK",
    "USD_SGD",
    "USD_THB",
    "USD_TRY",
    "USD_ZAR"
    """

    def tearDown(self):
        """Add new ID to the file below for future uses."""
        with open("used_own_ids.txt", "a") as f:
            f.write(str(int(self.last_own_id) + 1) + "\n")

    @property
    def last_own_id(self):
        with open("used_own_ids.txt") as f:
            last_own_id = f.read().split("\n")[-2]  # [-1] is blank string

        return last_own_id

    def test_get_trade_method(self):
        own_id = "USD_CAD_" + self.last_own_id
        self.oanda.create_market_order("USD_CAD", "BUY", 1, own_id=own_id)

        trade_details = self.oanda.get_trade(own_id=own_id)
        assert trade_details["trade"]["clientExtensions"]["id"] == own_id

    def test_get_all_trades_method(self):
        self.oanda.create_market_order("USD_CHF", "BUY", 1)

        open_trades = self.oanda.get_all_trades()
        assert len(open_trades["trades"]) >= 1

        trades_instrument_list = \
            [trade["instrument"] for trade in open_trades["trades"]]
        assert "USD_CHF" in trades_instrument_list

    def test_update_trade_method(self):
        own_id = "USD_CNH_" + self.last_own_id
        self.oanda.create_market_order("USD_CNH", "BUY", 1, own_id=own_id)

        pricing = self.oanda.get_pricing(["USD_CNH"])
        price = pricing["prices"][0]["bids"][0]["price"]
        stoploss = float(price) - 0.5
        takeprofit = float(price) + 0.5

        is_updated = self.oanda.update_trade(
            own_id=own_id, stoploss=stoploss, takeprofit=takeprofit)
        assert is_updated

        trade_details = self.oanda.get_trade(own_id=own_id)
        assert trade_details["trade"]["stopLossOrder"]["price"] == \
            str(stoploss)

    def test_update_trade_extensions_method(self):
        own_id = "USD_CZK_" + self.last_own_id
        self.oanda.create_market_order("USD_CZK", "BUY", 1, own_id=own_id)

        is_updated = self.oanda.update_trade_extensions(
            own_id=own_id, tag="foo", comment="bar")
        assert is_updated

        trade_details = self.oanda.get_trade(own_id=own_id)
        assert trade_details["trade"]["clientExtensions"]["tag"] == "foo"

    def test_close_trade_method(self):
        own_id = "USD_DKK_" + self.last_own_id
        self.oanda.create_market_order("USD_DKK", "BUY", 1, own_id=own_id)

        is_closed = self.oanda.close_trade(own_id=own_id)
        assert is_closed

        trade_details = self.oanda.get_trade(own_id=own_id)
        assert trade_details["trade"]["state"] == "CLOSED"

    def test_close_filtered_trades_method(self):
        own_id_1 = "USD_HKD_" + self.last_own_id
        self.oanda.create_market_order("USD_HKD", "BUY", 1, own_id=own_id_1)

        own_id_2 = "USD_HUF_" + self.last_own_id
        self.oanda.create_market_order("USD_HUF", "BUY", 1, own_id=own_id_2)

        self.oanda.close_filtered_trades(own_ids=[own_id_1, own_id_2])

        open_trades = self.oanda.get_all_trades()
        open_trades_own_ids_list = \
            [trade["clientExtensions"]["id"] for trade in
             open_trades["trades"]]
        assert own_id_1 not in open_trades_own_ids_list
        assert own_id_2 not in open_trades_own_ids_list

        self.oanda.close_filtered_trades(instrument="USD")

        open_trades = self.oanda.get_all_trades()
        assert not len(open_trades["trades"])

    def test_close_all_trades_method(self):
        self.oanda.create_market_order("USD_INR", "BUY", 1)
        self.oanda.close_all_trades()

        open_trades = self.oanda.get_all_trades()
        assert not len(open_trades["trades"])


if __name__ == "__main__":
    unittest.main()
