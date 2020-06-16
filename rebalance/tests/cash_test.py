import unittest

from rebalance import Cash
from rebalance import Price

from forex_python.converter import CurrencyRates

class TestCash(unittest.TestCase):

    def test_interface(self):
        """
        Test interface of Cash class.
        """
        amount = 20.4
        currency = "CAD"
        cash = Cash(amount = amount, currency = currency)
        self.assertEqual(cash.amount, amount)
        self.assertEqual(cash.currency, currency.upper())

        # currency coversion to itself
        self.assertEqual(cash.amount_in(currency), amount)

        ex_rate = CurrencyRates()
        self.assertEqual(cash.exchange_rate("usd"), ex_rate.get_rate(currency, "USD"))
        self.assertEqual(cash.amount_in("usd"), ex_rate.get_rate(currency, "USD")*amount)

class TestPrice(unittest.TestCase):

    def test_interface(self):
        """
        Test interface of Price class.
        """
        price = 20.4
        currency = "CAD"
        cash = Price(price = price, currency = currency)
        self.assertEqual(cash.price, price)
        self.assertEqual(cash.currency, currency.upper())

        # currency conversion to itself
        self.assertEqual(cash.price_in(currency), price)

        ex_rate = CurrencyRates()
        self.assertEqual(cash.price_in("usd"), ex_rate.get_rate(currency, "USD")*price)


if __name__ == '__main__':
    unittest.main()