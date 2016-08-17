import unittest

from requests import HTTPError

from oandav20.testing import TestCase, ID


class TestAccountMixin(TestCase):

    def tearDown(self):
        """Configure the margin rate back to 0.01"""
        self.oanda.configure_account(1)

    def test_available_accounts_method(self):
        account_ids = self.oanda.get_available_accounts()
        assert ID == account_ids["accounts"][0]["id"]

    def test_get_account_method(self):
        account_id = self.oanda.get_account()
        assert ID == account_id["account"]["id"]

    def test_get_account_summary_method(self):
        account_details = self.oanda.get_account_summary()
        assert ID == account_details["account"]["id"]

        another_id = "101-004-3881593-002"
        account_details = self.oanda.get_account_summary(account_id=another_id)
        assert another_id == account_details["account"]["id"]

        fake_id = "foo"

        with self.assertRaises(HTTPError):
            self.oanda.get_account_summary(account_id=fake_id)

    def test_get_instruments_method(self):
        single_instrument = self.oanda.get_instruments(["AUD_USD"])
        assert "AUD_USD" in single_instrument["instruments"][0]["name"]

        more_instruments = self.oanda.get_instruments(["AUD_USD", "EUR_USD"])
        assert "EUR_USD" in more_instruments["instruments"][1]["name"]

        all_instruments = self.oanda.get_instruments()
        assert "name" in all_instruments["instruments"][0]

        with self.assertRaises(ValueError):
            self.oanda.get_instruments(["foo"])

    def test_configure_account_method(self):
        is_configured = self.oanda.configure_account(5)
        assert is_configured

        with self.assertRaises(ValueError):
            self.oanda.configure_account("foo")


if __name__ == "__main__":
    unittest.main()
