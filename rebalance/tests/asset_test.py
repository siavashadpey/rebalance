import unittest

from rebalance import Asset
from rebalance import Price

import yfinance as yf

class TestAsset(unittest.TestCase):

    def test_interface(self):
        """
        Test the interface of Asset class.

        Primary methods.
        """

        ticker = "VCN.TO"
        quantity = 2
        asset = Asset(ticker, quantity)

        ticker_info = yf.Ticker(ticker).info

        self.assertEqual(asset.quantity, quantity)
        self.assertEqual(asset.price, yf.Ticker(ticker).info["ask"])
        self.assertEqual(asset.ticker, ticker)
        self.assertEqual(asset.currency, yf.Ticker(ticker).info["currency"])
        self.assertEqual(asset.market_value(), yf.Ticker(ticker).info["ask"]*quantity)

    def test_interface2(self):
        """
        Test the interface of Asset class. Part 2.

        Mainly related to currency conversion.
        """

        ticker = "TSLA" # currency: USD
        asset = Asset(ticker)
        quantity = 5
        asset.quantity = quantity

        self.assertEqual(asset.quantity, quantity)

        ticker_info = yf.Ticker(ticker).info
        price = Price(ticker_info["ask"], currency=ticker_info["currency"])
        
        self.assertEqual(asset.price_in("CAD"), price.price_in("CAD"))
        self.assertEqual(asset.market_value(), price.price*quantity)
        self.assertEqual(asset.market_value_in("CAD"), price.price_in("CAD")*quantity)


    def test_interface3(self):
        """
        Test the interface of Asset class. Part 3.

        Mainly related to buying units.
        """

        ticker = "ZAG.TO" # currency: CAD
        quantity = 10
        asset = Asset(ticker, quantity)

        ticker_info = yf.Ticker(ticker).info
        price = Price(ticker_info["ask"], currency=ticker_info["currency"])

        to_buy = 4
        self.assertEqual(asset.cost_of(to_buy), price.price*to_buy)
        self.assertEqual(asset.cost_of(to_buy, currency="USD"), price.price_in("USD")*to_buy)

        self.assertEqual(asset.buy(to_buy), price.price*to_buy)
        self.assertEqual(asset.quantity, quantity + to_buy)

        self.assertEqual(asset.buy(to_buy, currency="USD"), price.price_in("USD")*to_buy)
        self.assertEqual(asset.quantity, quantity + to_buy + to_buy)

if __name__ == '__main__':
    unittest.main()