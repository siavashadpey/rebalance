

from rebalance import Cash

from forex_python.converter import CurrencyRates

class Price:
    """
        
    """
    def __init__(self,
                 price = None,
                 currency = "CAD"
    ):
        if price is None:
            print("`price` argument must be specified.")
            raise TypeError

        self._price = price
        self._currency = currency.upper()

    @property
    def price(self):
        return self._price

    @property
    def currency(self):
        return self._currency

    def price_in(self, currency):
        
        currency_exchange = Cash.currency_rates.get_rate(self.currency, currency.upper())

        return currency_exchange*self._price
    
    
    

