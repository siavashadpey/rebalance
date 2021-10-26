import unittest
import math

import numpy as np

from rebalance import Portfolio
from rebalance import Asset

import yfinance as yf
from forex_python.converter import CurrencyRates


class TestPortfolio(unittest.TestCase):
    def test_cash_interface(self):
        """
        Test portfolio's interface related to Cash class.

        Adding cash of different currency individually to the portfolio.
        """
        p = Portfolio()
        amount1 = 500.15
        p.add_cash(amount1, "cad")
        amount2 = 200.00
        p.add_cash(amount2, "usd")

        self.assertEqual(p.cash["CAD"].amount, amount1)
        self.assertEqual(p.cash["USD"].amount, amount2)

    def test_cash_interface2(self):
        """
        Test portfolio's interface related to Cash class.

        Collectively adding cash to the portfolio.
        """
        p = Portfolio()
        amounts = [500.15, 200.00]
        currencies = ["CAD", "USD"]
        p.easy_add_cash(amounts, currencies)

        self.assertEqual(p.cash[currencies[0]].amount, amounts[0])
        self.assertEqual(p.cash[currencies[1]].amount, amounts[1])

    def test_asset_interface(self):
        """
        Test portfolio's interface related to Asset class.

        Adding assets individually to the portfolio.
        """
        p = Portfolio()

        ticker = "VCN.TO"
        quantity = 2
        ticker_info = yf.Ticker(ticker).info
        price = ticker_info["regularMarketPrice"]
        asset = Asset(ticker=ticker, quantity=quantity)

        p.add_asset(asset)
        self.assertEqual(asset.ticker, p.assets[ticker].ticker)
        self.assertEqual(asset.quantity, p.assets[ticker].quantity)
        self.assertEqual(asset.price, p.assets[ticker].price)

        ticker = "ZAG.TO"
        quantity = 20
        asset2 = Asset(ticker=ticker, quantity=quantity)
        p.add_asset(asset2)

        self.assertEqual(asset2.ticker, p.assets[ticker].ticker)
        self.assertEqual(asset2.quantity, p.assets[ticker].quantity)
        self.assertEqual(asset2.price, p.assets[ticker].price)

    def test_asset_interface2(self):
        """
        Test portfolio's interface related to Asset class.

        Collectively adding assets to the portfolio.
        """

        p = Portfolio()

        tickers = ["VCN.TO", "ZAG.TO"]
        quantities = [2, 20]
        p.easy_add_assets(tickers=tickers, quantities=quantities)

        n = len(tickers)
        for i in range(n):
            self.assertEqual(tickers[i], p.assets[tickers[i]].ticker)
            self.assertEqual(quantities[i], p.assets[tickers[i]].quantity)
            self.assertEqual(
                yf.Ticker(tickers[i]).info["regularMarketPrice"], p.assets[tickers[i]].price)

    def test_portfolio_value(self):
        """
        Test total market value, total cash value, and total value methods.
        """

        p = Portfolio()

        tickers = ["VCN.TO", "ZAG.TO", "XAW.TO", "TSLA"]
        quantities = [2, 20, 10, 4]
        p.easy_add_assets(tickers=tickers, quantities=quantities)

        mv = p.market_value("CAD")

        total_mv = np.sum(
            [asset.market_value_in("CAD") for asset in p.assets.values()])

        self.assertAlmostEqual(mv, total_mv, 1)

        amounts = [500.15, 200.00]
        currencies = ["CAD", "USD"]
        p.easy_add_cash(amounts, currencies)

        cv = p.cash_value("CAD")

        usd_to_cad = CurrencyRates().get_rate("USD", "CAD")
        total_cv = np.sum(amounts[0] + amounts[1] * usd_to_cad)
        self.assertAlmostEqual(cv, total_cv, 1)

        self.assertAlmostEqual(p.value("CAD"), total_mv + total_cv, 1)

    def test_asset_allocation(self):
        """
        Test asset allocation method.
        """
        p = Portfolio()

        tickers = ["VCN.TO", "ZAG.TO", "XAW.TO", "TSLA"]
        quantities = [2, 20, 10, 4]
        p.easy_add_assets(tickers=tickers, quantities=quantities)

        asset_alloc = p.asset_allocation()
        self.assertAlmostEqual(sum(asset_alloc.values()), 100., 7)

        rates = CurrencyRates()

        prices = [
            yf.Ticker(ticker).info["regularMarketPrice"] *
            rates.get_rate(yf.Ticker(ticker).info["currency"], "CAD")
            for ticker in tickers
        ]
        total = np.sum(np.asarray(quantities) * np.asarray(prices))
        n = len(tickers)
        for i in range(n):
            self.assertAlmostEqual(asset_alloc[tickers[i]],
                                   quantities[i] * prices[i] / total * 100., 1)

    def test_exchange(self):
        """
        Test currency exchange in Portfolio.
        """

        p = Portfolio()

        amounts = [500.15, 200.00]
        currencies = ["CAD", "USD"]
        p.easy_add_cash(amounts, currencies)

        cad_to_usd = CurrencyRates().get_rate("CAD", "USD")

        p.exchange_currency(to_currency="CAD",
                            from_currency="USD",
                            to_amount=100)
        self.assertAlmostEqual(p.cash["CAD"].amount, 500.15 + 100., 1)
        self.assertAlmostEqual(p.cash["USD"].amount, 200. - 100. * cad_to_usd,
                               1)

        p.exchange_currency(from_currency="USD",
                            to_currency="CAD",
                            from_amount=50)
        self.assertAlmostEqual(p.cash["CAD"].amount,
                               500.15 + 100 + 50 / cad_to_usd, 1)
        self.assertAlmostEqual(p.cash["USD"].amount,
                               200. - 100. * cad_to_usd - 50, 1)

        # error handling:
        with self.assertRaises(Exception):
            p.exchange_currency(to_currency="CAD",
                                from_currency="USD",
                                to_amount=100,
                                from_amount=20)

        # error handling
        with self.assertRaises(Exception):
            p.exchange_currency(to_currency="CAD", from_currency="USD")

    def test_rebalancing(self):
        """
        Test rebalancing algorithm.

        This might break over time as prices increase.
        If we have enough cash though, the optimizer should ideally
        be able to match the target asset allocation
        pretty closely
        """

        p = Portfolio()

        tickers = ["XBB.TO", "XIC.TO", "ITOT", "IEFA", "IEMG"]
        quantities = [36, 64, 32, 8, 7]
        p.easy_add_assets(tickers=tickers, quantities=quantities)
        p.add_cash(3000, "USD")
        p.add_cash(515.21, "CAD")
        p.add_cash(5.00, "GBP")
        p.selling_allowed = True

        self.assertTrue(p.selling_allowed)

        # different order than tickers.
        # rebalance method should be able to handle such a case
        target_asset_alloc = {
            "XBB.TO": 20,
            "XIC.TO": 20,
            "IEFA": 20,
            "ITOT": 36,
            "IEMG": 4
        }

        initial_value = p.value("CAD")
        (_, _, _, max_diff) = p.rebalance(target_asset_alloc, verbose=True)
        final_value = p.value("CAD")
        self.assertAlmostEqual(initial_value, final_value, 1)
        self.assertLessEqual(max_diff, 2.)

        # Error handling
        with self.assertRaises(Exception):
            target_asset_alloc = {
                "XBB.TO": 20,
                "XIC.TO": 20,
                "IEFA": 20,
            }
            p.rebalance(target_asset_alloc)

    def test_rebalancing2(self):
        """
        Test rebalancing algorithm. Part 2.

        Cash is not in the same currency as the assets.
        """
        p = Portfolio()

        p.add_cash(200., "USD")
        p.add_cash(250., "GBP")

        tickers = ["VCN.TO", "XAW.TO", "ZAG.TO"]
        quantities = [5, 12, 20]
        p.easy_add_assets(tickers=tickers, quantities=quantities)

        target_asset_alloc = {
            "VCN.TO": 40.0,
            "ZAG.TO": 40.0,
            "XAW.TO": 20.0,
        }

        initial_value = p.value("CAD")
        p.selling_allowed = False
        (_, prices, _, _) = p.rebalance(target_asset_alloc, verbose=True)
        final_value = p.value("CAD")
        self.assertAlmostEqual(initial_value, final_value, -1)

        # The prices should be in the tickers' currency
        for ticker in tickers:
            self.assertEqual(prices[ticker][1], "CAD")

        # Since there was no CAD to start off with,
        # there should be none after rebalacing either
        # (i.e. amount converted to CAD should be the amount used to purchase CAD assets)
        self.assertAlmostEqual(p.cash["CAD"].amount, 0., 1)


if __name__ == '__main__':
    unittest.main()
