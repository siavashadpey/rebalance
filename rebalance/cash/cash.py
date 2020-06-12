
from forex_python.converter import CurrencyRates

#TODO: documentation 

class Cash:
    """
    An instance of Cash holds an amount and a currency.

    It is used as part of an asset class.

    """
    currency_rates = CurrencyRates()
    def __init__(self,
                 amount = None,
                 currency = "CAD"
    ):
        if amount is None:
            print("`amount` argument must be specified.")
            raise TypeError

        self._amount = amount
        self._currency = currency.upper()


    @property
    def amount(self):
        """
            Gets and sets amount of cash in its own currency.
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def currency(self):
        """
            Gets currency of cash.
        """
        return self._currency

    def amount_in(self, currency):
        """
            Gets amount of cash in specified currency.
        """

        currency_exchange = Cash.currency_rates.get_rate(self.currency, currency.upper())

        return currency_exchange*self._amount
