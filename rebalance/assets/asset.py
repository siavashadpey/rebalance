
from rebalance import Price

import yfinance as yf

#TODO: documentation

class Asset:
    """
    Asset class.

    Holds the name, number of units, and the :class:`.Price` of the asset.

    """
    def __init__(self, ticker, quantity):
        """
        Initialization.

        Args:
            ticker (str): Ticker of the asset.
            quantity (int): Number of units of the asset.
        """

        assert ticker is not None, "ticker symbol is a mandatory argument."
        assert isinstance(quantity, int), "quantity must be integer."

        self._ticker = ticker
        self._quantity = quantity
        ticker_info = yf.Ticker(self._ticker).info
        self._price = Price(ticker_info["regularMarketOpen"], ticker_info["currency"])
    
    def market_value(self):
        """
        Computes the market value of the asset. 

        Returns:
            float: Market value of the asset (in asset's own currency).
        """
        return self.price*self._quantity

    def market_value_in(self, currency):
        """
        Computes the market value of the asset in specified currency. 

        Args:
            currency (str): Currency in which to obtain market value.

        Returns:
            float: Market value of the asset.
        """
        return self._price.price_in(currency)*self._quantity

    @property
    def quantity(self):
        """ (int): Number of units of the asset. """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        assert isinstance(quantity, int), "quantity must be integer." 
        self._quantity = quantity

    def buy(self, quantity, currency=None):
        """
            Buys a specified amount of the asset.

            Args:
                quantity (int): Quantity to buy.
                currency (str, optional): Currency in which to obtain cost. Defaults to asset's own currency.

            Returns:
                (float): Cost of the units bought in specified ``currency``.
        """
        self._quantity += quantity
        if currency is None:
            return self._price.price*quantity
        else:
            return self._price.price_in(currency)*quantity

    
    @property
    def price(self):
        """ 
        (float): Price of the asset (in asset's own currency). 
        """
        return self._price.price

    def price_in(self, currency):
        """ 
        Price of the asset in specified currency. 

        Args:
            currency (str): Currency in which to obtain price of asset.
        """
        return self._price.price_in(currency)

    @property
    def currency(self):
        """ 
        (str): Currency of the asset. 
        """
        return self._price.currency

    @property
    def ticker(self):
        """
        (str): Ticker of the asset.
        """
        return self._ticker

    def __str__(self):
        return yf.Ticker(self._ticker).info['shortName'] + "(" + self._ticker + ")" 