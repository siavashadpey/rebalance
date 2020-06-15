import unittest
import math

import numpy as np

from rebalance import Portfolio
from rebalance import Asset

import yfinance as yf
from forex_python.converter import CurrencyRates

class TestPortfolio(unittest.TestCase):

    def test_cash_interface(self):
        p = Portfolio()
        amount1 = 500.15
        p.add_cash(amount1, "cad")
        amount2 = 200.00
        p.add_cash(amount2, "usd")

        self.assertEqual(p.cash["CAD"].amount, amount1)
        self.assertEqual(p.cash["USD"].amount, amount2)

    def test_cash_interface2(self):
        p = Portfolio()
        amounts = [500.15, 200.00]
        currencies = ["CAD", "USD"]
        p.easy_add_cash(amounts, currencies)

        self.assertEqual(p.cash[currencies[0]].amount, amounts[0])
        self.assertEqual(p.cash[currencies[1]].amount, amounts[1])


    def test_asset_interface(self):
        p = Portfolio()

        ticker = "VCN.TO"
        quantity = 2
        ticker_info = yf.Ticker(ticker).info
        price = ticker_info["ask"]
        asset = Asset(ticker=ticker, quantity = quantity)

        p.add_asset(asset)
        self.assertEqual(asset.ticker, p.assets[ticker].ticker)
        self.assertEqual(asset.quantity, p.assets[ticker].quantity)
        self.assertEqual(asset.price, p.assets[ticker].price)

        ticker = "ZAG.TO"
        quantity = 20
        asset2 = Asset(ticker=ticker, quantity = quantity)
        p.add_asset(asset2)

        self.assertEqual(asset2.ticker, p.assets[ticker].ticker)
        self.assertEqual(asset2.quantity, p.assets[ticker].quantity)
        self.assertEqual(asset2.price, p.assets[ticker].price)

    def test_asset_interface2(self):
        p = Portfolio()

        tickers = ["VCN.TO", "ZAG.TO"]
        quantities = [2, 20]
        p.easy_add_assets(tickers=tickers, quantities = quantities)

        for i in range(len(tickers)):
            self.assertEqual(tickers[i], p.assets[tickers[i]].ticker)
            self.assertEqual(quantities[i], p.assets[tickers[i]].quantity)
            self.assertEqual(yf.Ticker(tickers[i]).info["ask"], p.assets[tickers[i]].price)

    def test_asset_allocation(self):
        p = Portfolio()

        tickers = ["VCN.TO", "ZAG.TO", "XAW.TO", "TSLA"]
        quantities = [2, 20, 10, 4]
        p.easy_add_assets(tickers=tickers, quantities = quantities)


        asset_alloc = p.asset_allocation()
        self.assertAlmostEqual(sum(asset_alloc.values()), 100., 7)

        rates = CurrencyRates()

        prices = [yf.Ticker(ticker).info["ask"]*rates.get_rate(yf.Ticker(ticker).info["currency"], "CAD") for ticker in tickers]
        total = np.sum(np.asarray(quantities)*np.asarray(prices))
        for i in range(len(tickers)):
            self.assertAlmostEqual(asset_alloc[tickers[i]], quantities[i]*prices[i]/total*100., 1)

    def test_rebalancing(self):
        p = Portfolio()

        tickers = ["VCN.TO", "ZAG.TO", "XAW.TO"]
        quantities = [5, 20, 12]
        p.easy_add_assets(tickers=tickers, quantities = quantities)
        p.add_cash(515.21, "CAD")
        p.selling_allowed = True
        #for ticker in p.assets.keys():
        #    print(ticker, p.assets[ticker].price)

        target_allocation = {"VCN.TO": 20., "ZAG.TO": 40., "XAW.TO": 40.}
        p.rebalance(target_allocation)


if __name__ == '__main__':
    unittest.main()