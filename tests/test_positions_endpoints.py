import unittest

from oandav20.testing import TestCase


class TestPositionsMixin(TestCase):

    def test_get_positions_method(self):
        positions = self.oanda.get_positions()
        assert len(positions["positions"]) > 0


if __name__ == "__main__":
    unittest.main()
