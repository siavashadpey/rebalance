import unittest

from rebalance import Cash
from rebalance import Price

class TestCash(unittest.TestCase):

    def test_interface(self):
        amount = 20.4
        currency = "cad"
        cash = Cash(amount = amount, currency = currency)
        self.assertEqual(cash.amount, amount)
        self.assertEqual(cash.currency, currency.upper())

class TestPrice(unittest.TestCase):

    def test_interface(self):
        price = 20.4
        currency = "cad"
        cash = Price(price = price, currency = currency)
        self.assertEqual(cash.price, price)
        self.assertEqual(cash.currency, currency.upper())


if __name__ == '__main__':
    unittest.main()