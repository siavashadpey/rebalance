
from rebalance import Price

import yfinance as yf

#TODO: documentation

class Asset:
    """
    Asset class.

    Holds the name, quantity, and the price of the asset.

    """
    def __init__(self, 
                 ticker: str = None, 
                 quantity: int = 1
    ):

        """ 
        Kwargs:
            name: Name of the asset.
            quantity: Quantity owned of the asset.
            price: Price of the asset.
            currency: Currency of the asset.
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
            float. Market value of the asset.
        """
        return self.price*self._quantity

    def market_value_in(self, currency):
        """
        Computes the market value of the asset. 

        Returns:
            float. Market value of the asset.
        """
        return self._price.price_in(currency)*self._quantity

    @property
    def quantity(self):
        """ Returns the quantity of the asset. """
        return self._quantity

    @quantity.setter
    def quantity(self, 
                 quantity: int
    ):
        assert isinstance(quantity, int), "quantity must be integer." 
        self._quantity = quantity

    def buy(self, quantity, currency=None):
        self._quantity += quantity
        if currency is None:
            return self._price.price*quantity
        else:
            return self._price.price_in(currency)*quantity

    
    @property
    def price(self):
        """ Returns the price of the asset. """
        return self._price.price

    def price_in(self, currency):
        """ Returns the price of the asset. """
        return self._price.price_in(currency)

    @property
    def currency(self):
        """ Returns the currency of the asset. """
        return self._price.currency

    @property
    def ticker(self):
        return self._ticker

    def __str__(self):
        return yf.Ticker(self._ticker).info['shortName'] + "(" + self._ticker + ")" 