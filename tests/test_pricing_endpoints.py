import unittest

from oandav20.testing import TestCase


class TestPricingMethods(TestCase):
    """Test for the PricingMixin class."""

    def test_get_pricing_for_single_instrument(self):
        """Testing pricing for one instrument in the 'get_pricing' method."""
        response = self.oanda.get_pricing(["AUD_USD"])

        self.assertTrue("AUD_USD", response["prices"][0]["instrument"])

    def test_get_pricing_for_more_instruments(self):
        """Testing pricing for more instruments in the 'get_pricing' method."""
        response = self.oanda.get_pricing(["EUR_USD", "GBP_USD"])

        self.assertTrue("GBP_USD", response["prices"][1]["instrument"])

    def test_get_pricing_for_invalid_instruments(self):
        """Testing invalid instrment code passed to the 'get_pricing'
        method."""
        with self.assertRaises(ValueError):
            self.oanda.get_pricing(["foo"])


if __name__ == "__main__":
    unittest.main()
