import unittest

from rebalance import Asset

import yfinance as yf

class TestAsset(unittest.TestCase):

    def test_interface(self):
        ticker = "VCN.TO"
        quantity = 2
        ticker_info = yf.Ticker(ticker).info
        price = ticker_info["ask"]
        asset = Asset(ticker, quantity)
        self.assertEqual(asset.quantity, quantity)
        self.assertEqual(asset.price, price)
        self.assertEqual(asset.ticker, ticker)
        self.assertEqual(asset.market_value(), price*quantity)
        self.assertEqual(asset.currency, ticker_info["currency"])


if __name__ == '__main__':
    unittest.main()