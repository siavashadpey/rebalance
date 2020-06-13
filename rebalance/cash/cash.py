
from forex_python.converter import CurrencyRates

#TODO: documentation 

class Cash:
    """
    An instance of :class:`Cash` holds an amount and a currency.

    Attributes
        currency_rates (forex_python.converter) : Used for currency conversion.

    """
    currency_rates = CurrencyRates()

    def __init__(self, amount = None, currency = "CAD"):
        """
        Initialization.

        Args:
            amount (float, optional): Amount of cash.
            currency (str, optional): Currency of cash. Defaults to "CAD" .
        """
        if amount is None:
            print("`amount` argument must be specified.")
            raise TypeError

        self._amount = amount
        self._currency = currency.upper()


    @property
    def amount(self):
        """
        (float): Amount of cash.
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def currency(self):
        """
        (str): Currency of cash.
        """
        return self._currency

    def amount_in(self, currency):
        """
        Converts amount of cash in specified currency.

        Args:
            currency (str): Currency in which to convert the amount of cash.

        Returns:
            (float): Amount of cash in specified currency.
        """

        currency_exchange = Cash.currency_rates.get_rate(self.currency, currency.upper())

        return currency_exchange*self._amount
