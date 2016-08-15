import unittest

from requests import HTTPError

from oandav20.testing import TestCase, ID


class TestAccountMethods(TestCase):
    """Tests for the AccountMixin class."""

    def test_available_accounts(self):
        """Testing the 'get_available_accounts' method."""
        response = self.oanda.get_available_accounts()

        self.assertEqual(ID, response["accounts"][0]["id"])

    def test_full_account_info(self):
        """Testing the 'get_account' method."""
        response = self.oanda.get_account()

        self.assertEqual(ID, response["account"]["id"])

    def test_account_summary(self):
        """Testing the 'get_account_summary' method."""
        response = self.oanda.get_account_summary()

        self.assertEqual(ID, response["account"]["id"])

    def test_different_account_id(self):
        """Testing different account ID passed to the 'get_account_summary'
        method.

        The same behaviour would be for any method using the 'account_id'
        parameter."""
        another_id = "101-004-3881593-002"
        response = self.oanda.get_account_summary(account_id=another_id)

        self.assertEqual(another_id, response["account"]["id"])

    def test_fake_account_id(self):
        """Testing fake account id passed to the 'get_account_summary'
        method."""
        fake_id = "foo"

        with self.assertRaises(HTTPError):
            self.oanda.get_account_summary(account_id=fake_id)

    def test_info_for_all_instruments(self):
        """Testing the 'get_instruments' method without passing any instrument
        codes."""
        response = self.oanda.get_instruments()

        self.assertIn("name", response["instruments"][0])

    def test_info_for_several_instruments(self):
        """Testing several instrument codes passed to the 'get_instruments'
        method."""
        response = self.oanda.get_instruments(["AUD_USD", "EUR_USD"])

        self.assertEqual("EUR_USD", response["instruments"][1]["name"])

    def test_info_for_one_instrument(self):
        """Testing one instrument code passed to the 'get_instruments' method.
        """
        response = self.oanda.get_instruments(["AUD_USD"])

        self.assertEqual("AUD_USD", response["instruments"][0]["name"])

    def test_invalid_instrument_code(self):
        """Testing invalid instrument code passed to the 'get_instruments'
        method."""
        with self.assertRaises(ValueError):
            self.oanda.get_instruments(["foo"])

    def test_configure_different_margin_rate(self):
        """Testing the 'configure_account' method."""
        response = self.oanda.configure_account(5)

        self.assertTrue(response)

    def test_configure_invalid_margin_rate(self):
        """Testing invalid margin rate passed to the 'configure_account'
        method."""
        with self.assertRaises(ValueError):
            response = self.oanda.configure_account("foo")

    def tearDown(self):
        """Configure back the margin rate to 0.01"""
        self.oanda.configure_account(1)


if __name__ == "__main__":
    unittest.main()
