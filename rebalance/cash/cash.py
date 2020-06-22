from forex_python.converter import CurrencyRates


class Cash:
    """
    An instance of :class:`Cash` holds an amount and a currency.

    Attributes
        currency_rates (forex_python.converter) : Used for currency conversion.

    """
    currency_rates = CurrencyRates()

    def __init__(self, amount, currency="CAD"):
        """
        Initialization.

        Args:
            amount (float): Amount of cash.
            currency (str, optional): Currency of cash. Defaults to "CAD".
        """

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

        return self.exchange_rate(currency) * self._amount

    def exchange_rate(self, currency):
        """
        Obtain the exchange rate from ``cash``'s own currency to specified currency.

        Args:
            currency (str): Currency.

        Returns:
            (float): exchange rate.
        """

        return Cash.currency_rates.get_rate(self.currency, currency.upper())
