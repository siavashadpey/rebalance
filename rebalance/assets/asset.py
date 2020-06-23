from rebalance import Price

import yfinance as yf


class Asset:
    """
    Asset class.

    Holds the name, number of units, and the :class:`.Price` of the asset.

    """
    def __init__(self, ticker, quantity=0):
        """
        Initialization.

        Args:
            ticker (str): Ticker of the asset.
            quantity (int, optional): Number of units of the asset. Default is zero.
        """

        assert ticker is not None, "ticker symbol is a mandatory argument."
        assert isinstance(quantity, int), "quantity must be integer."

        self._ticker = ticker
        self._quantity = quantity
        ticker_info = yf.Ticker(self._ticker).info

        # we set the price to ask
        self._price = Price(ticker_info["ask"], ticker_info["currency"])

    @property
    def quantity(self):
        """ (int): Number of units of the asset. """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        assert isinstance(quantity, int), "quantity must be integer."
        self._quantity = quantity

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

    def market_value(self):
        """
        Computes the market value of the asset. 

        Returns:
            float: Market value of the asset (in asset's own currency).
        """
        return self.price * self._quantity

    def market_value_in(self, currency):
        """
        Computes the market value of the asset in specified currency. 

        Args:
            currency (str): Currency in which to obtain market value.

        Returns:
            float: Market value of the asset.
        """
        return self._price.price_in(currency) * self._quantity

    def buy(self, quantity, currency=None):
        """
        Buys (or sells) a specified amount of the asset.

        Args:
            quantity (int): If positive, it is the quantity to buy. If negative, it is the quantity to sell.
            currency (str, optional): Currency in which to obtain cost. Defaults to asset's own currency.

        Returns:
            (float): Cost of the units bought in specified ``currency``.
        """
        self._quantity += quantity
        if currency is None:
            return self._price.price * quantity
        
        return self._price.price_in(currency) * quantity

    def cost_of(self, units, currency=None):
        """
        Computes the cost to purchase the specified number of units.

        Args:
            units (int): Units interested in purchasing.
            currency (str, optional): Currency in which to convert the cost. Default is asset's own currency.

        Returns:
            (float): Cost of the purchase.
        """
        if currency is None:
            return self.price * units
      
        return self.price_in(currency) * units

    def __str__(self):
        return yf.Ticker(
            self._ticker).info['shortName'] + "(" + self._ticker + ")"
