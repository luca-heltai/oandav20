import unittest

from oandav20.testing import TestCase


class TestPositionsMethods(TestCase):
    """Tests for the PositionsMixin class."""

    def test_get_positions(self):
        """Test the 'get_positions' method."""
        response = self.oanda.get_positions()

        self.assertGreater(len(response["positions"]), 0)


if __name__ == "__main__":
    unittest.main()
