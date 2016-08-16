import unittest

from requests import HTTPError

from oandav20.testing import TestCase, ID


class TestAccountMethods(TestCase):
    """Tests for the AccountMixin class."""

    def tearDown(self):
        """Configure the margin rate back to 0.01"""
        self.oanda.configure_account(1)

    def test_available_accounts(self):
        """Test the 'get_available_accounts' method."""
        response = self.oanda.get_available_accounts()

        self.assertEqual(ID, response["accounts"][0]["id"])

    def test_full_account_info(self):
        """Test the 'get_account' method."""
        response = self.oanda.get_account()

        self.assertEqual(ID, response["account"]["id"])

    def test_account_summary(self):
        """Test the 'get_account_summary' method."""
        response = self.oanda.get_account_summary()

        self.assertEqual(ID, response["account"]["id"])

    def test_different_account_id(self):
        """Test different account ID passed to the 'get_account_summary'
        method.

        The same behaviour would be for any method using the 'account_id'
        parameter."""
        another_id = "101-004-3881593-002"
        response = self.oanda.get_account_summary(account_id=another_id)

        self.assertEqual(another_id, response["account"]["id"])

    def test_fake_account_id(self):
        """Test fake account id passed to the 'get_account_summary'
        method."""
        fake_id = "foo"

        with self.assertRaises(HTTPError):
            self.oanda.get_account_summary(account_id=fake_id)

    def test_info_for_all_instruments(self):
        """Test the 'get_instruments' method without passing any instrument
        codes."""
        response = self.oanda.get_instruments()

        self.assertIn("name", response["instruments"][0])

    def test_info_for_several_instruments(self):
        """Test several instrument codes passed to the 'get_instruments'
        method."""
        response = self.oanda.get_instruments(["AUD_USD", "EUR_USD"])

        self.assertEqual("EUR_USD", response["instruments"][1]["name"])

    def test_info_for_one_instrument(self):
        """Test one instrument code passed to the 'get_instruments' method.
        """
        response = self.oanda.get_instruments(["AUD_USD"])

        self.assertEqual("AUD_USD", response["instruments"][0]["name"])

    def test_invalid_instrument_code(self):
        """Test invalid instrument code passed to the 'get_instruments'
        method."""
        with self.assertRaises(ValueError):
            self.oanda.get_instruments(["foo"])

    def test_configure_different_margin_rate(self):
        """Test the 'configure_account' method."""
        response = self.oanda.configure_account(5)

        self.assertTrue(response)

    def test_configure_invalid_margin_rate(self):
        """Test invalid margin rate passed to the 'configure_account'
        method."""
        with self.assertRaises(ValueError):
            self.oanda.configure_account("foo")


if __name__ == "__main__":
    unittest.main()
