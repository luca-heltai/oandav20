import unittest

from oandav20 import Oanda

TOKEN = "daa5353bd6b4f58bfdf12cfb92cfd3a9-1db8ed54245cc325f87287a6f5863ca3"
ID = "101-004-3881593-001"


class TestCase(unittest.TestCase):
    """Custom TestCase class for unittesting package Oandav20."""

    @classmethod
    def setUpClass(cls):
        """Create an HTTP session connection with the Oanda server."""
        cls.oanda = Oanda("DEMO", TOKEN, ID)

    @classmethod
    def tearDownClass(cls):
        """Close all pending orders, open trades if any exists and close the
        HTTP session connection.
        """
        cls.oanda.client.close()
