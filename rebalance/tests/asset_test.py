import unittest

from rebalance import Asset

import yfinance as yf

class TestAsset(unittest.TestCase):

    def test_interface(self):
        ticker = "VCN.TO"
        quantity = 2
        ticker_info = yf.Ticker(ticker).info
        asset = Asset(ticker, quantity)
        self.assertEqual(asset.quantity, quantity)
        self.assertEqual(asset.price, yf.Ticker(ticker).info["ask"])
        self.assertEqual(asset.ticker, ticker)
        self.assertEqual(asset.market_value(), yf.Ticker(ticker).info["ask"]*quantity)
        self.assertEqual(asset.currency, yf.Ticker(ticker).info["currency"])


if __name__ == '__main__':
    unittest.main()