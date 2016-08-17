import unittest

from oandav20.testing import TestCase


class TestPricingMixin(TestCase):

    def test_get_pricing_method(self):
        single_instrument = self.oanda.get_pricing(["AUD_USD"])
        assert "AUD_USD" in single_instrument["prices"][0]["instrument"]

        more_instruments = self.oanda.get_pricing(["AUD_USD", "EUR_USD"])
        assert "EUR_USD" in more_instruments["prices"][1]["instrument"]

        with self.assertRaises(ValueError):
            self.oanda.get_pricing(["foo"])


if __name__ == "__main__":
    unittest.main()
