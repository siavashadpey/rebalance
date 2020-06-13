
import copy 
import math
from typing import Sequence

import numpy as np
from scipy.optimize import minimize

from rebalance import Asset
from rebalance import Cash
from rebalance import Price

#TODO: documentation

class Portfolio:
    """
    Portfolio class.

    Defines a :class:`.Portfolio` of :class:`.Asset` s and :class:`.Cash` and performs rebalancing of the portfolio.

    """

    _common_currency = "CAD"
    def __init__(self):
        """
        Initialization.
        """
        self._assets = {}
        self._cash = {}
        self._is_selling_allowed = False

    @property
    def cash(self):
        """
        Cash: Portfolio's dictionary of cash.
        """
        
        return self._cash

    @cash.setter
    def cash(self, cash):
        self._cash = cash

    def add_cash(self, amount, currency):
        """
        Adds cash to portfolio.
        
        Args:
            amount (float) : Amount of cash
            currency (str) : Currency of cash
        """

        # TODO: if existing currency, add amount to existing amount
        self._cash[currency.upper()] = Cash(amount, currency)

    def easy_add_cash(self, amounts, currencies):
        """
        An easy way of adding cash of various currencies to portfolio.

        Args:
            amounts (Sequence[float]): Amounts of cash from different curriencies.
            currencies (Sequence[str]): Specifies curriency of each of the amounts. Must be  in the same order as ``amounts``.

        """
        assert len(amounts) == len(currencies), "`amounts` and `currencies` should be of the same length."
        for amount, currency in zip(amounts, currencies):
            self._cash[currency.upper()] = Cash(amount, currency)

    @property
    def assets(self):
        """ 
        Dict[str, Asset]: Dictionary of assets in portfolio. The keys of the dictionary are the tickers of the assets.

        
        No setter allowed.
        """
        return self._assets

    @property
    def selling_allowed(self):
        """
        bool: Flag indicating if selling of assets is allowed or not when rebalancing portfolio.
        """
        return self._is_selling_allowed

    @selling_allowed.setter
    def selling_allowed(self, flag):
        self._is_selling_allowed = flag
    

    def add_asset(self, asset):
        """
        Adds specified :class:`.Asset` to the portfolio.

        Args:
            asset (Asset): Asset to add to portfolio.
        """
        self._assets[asset.ticker] = copy.deepcopy(asset)

    def easy_add_assets(self, tickers, quantities):
        """
        An easy way to add multiple assets to portfolio.

        Args:
            tickers (Sequence[str]): Ticker of assets in portfolio.
            quantities (Sequence[float]): Quantities of respective assets in portfolio. Must be in the same order as ``tickers``.
        """

        assert len(tickers) == len(quantities), \
               "`names` and `quantities` must be of the same length."

        for ticker, quantity in zip(tickers, quantities):
            self._assets[ticker] = Asset(ticker, quantity)

    def asset_allocation(self):
        """
        Computes the portfolio's asset allocation.


        Returns: 
            Dict[str, Asset]: Asset allocation of the portfolio (in %). The keys of the dictionary are the tickers of the assets.
        """
        
        # Obtain all market values in 1 currency (doesn't matter which) 
        total_value = 0.
        for asset in self._assets.values():
            total_value += asset.market_value_in(Portfolio._common_currency)

        asset_allocation = {}
        for name, asset in self._assets.items():
            asset_allocation[name] = asset.market_value_in(Portfolio._common_currency)/total_value*100.

        return asset_allocation

    def rebalance(self, target_allocation):

        """
            Rebalances the portfolio using the specified target allocation, the portfolio's current allocation,
            and the available cash.

            Args:
                target_allocation (Dict[str, float]): Target asset allocation of the portfolio (in %). The keys of the dictionary are the tickers of the assets.
        """

        # TODO: order target_allocation dict in the same order as assets dict
        target_allocation_np = np.fromiter(target_allocation.values(), dtype=float)

        assert abs(np.sum(target_allocation_np)-100.) <= 1E-2, "target allocation must sum up to 100%."

        # Make a new instance of portfolio
        # This is the one that is going to be rebalanced
        # We do not modify the current portfolio
        balanced_portfolio = copy.deepcopy(self)

        # If sell is  allowed, "sell everything" in new portfolio
        if self._is_selling_allowed:
            balanced_portfolio._sell_everything()

        # Convert all cash to one currency
        total_cash = 0.
        for cash in balanced_portfolio.cash.values():
            total_cash += cash.amount_in(Portfolio._common_currency)
        balanced_portfolio.cash = {Portfolio._common_currency: Cash(total_cash, balanced_portfolio._common_currency)}

        # Solve optimization problem
        nb_assets = len(balanced_portfolio._assets)
        bound = (0.00, total_cash)
        bounds = ((bound,)*nb_assets)
        constraints = [{'type': 'ineq', 'fun': lambda new_asset_values: balanced_portfolio.cash[Portfolio._common_currency].amount - np.sum(new_asset_values)}] # Can't buy more than available cash
        new_asset_values0 = np.ones(nb_assets)
        current_asset_values = np.array([asset.market_value_in(Portfolio._common_currency) for asset in balanced_portfolio.assets.values()])
        solution = minimize(balanced_portfolio._rebalance_objective_function, new_asset_values0, args=(current_asset_values, target_allocation_np), method='SLSQP', bounds=bounds, constraints=constraints)

        # Buy assets based on optimization solution
        quantities_to_buy = np.zeros_like(solution.x)
        investment_amount = np.zeros_like(solution.x)
        for i, ticker in zip(range(nb_assets), balanced_portfolio.assets.keys()):
            quantities_to_buy[i] = math.floor(solution.x[i]/balanced_portfolio.assets[ticker].price_in(Portfolio._common_currency))
            balanced_portfolio._buy_asset(ticker, quantities_to_buy[i])
            if self._is_selling_allowed:
                quantities_to_buy[i] -= self._assets[ticker].quantity
            investment_amount[i] = quantities_to_buy[i]*balanced_portfolio.assets[ticker].price


        # TODO: Compute total cash needed per currency

        # TODO: Compute currency exchanges needed and output this (if any)

        old_asset_allocation = self.asset_allocation()
        new_asset_allocation = balanced_portfolio.asset_allocation()

        # Print shares to buy, cost, new allocation, old allocation target, and target allocation
        print(" Ticker     Quantity   Amount   Currency   Old allocation   New allocation   Target allocation")
        print("            to buy      ($)                    (%)              (%)                (%)")
        print("----------------------------------------------------------------------------------------------")
        for i, ticker in zip(range(nb_assets), balanced_portfolio.assets.keys()):
            print("%s      %3.d        %6.2f    %s            %2.f               %2.f                 %2.f" % (ticker, quantities_to_buy[i], investment_amount[i], balanced_portfolio.assets[ticker].currency, old_asset_allocation[ticker], new_asset_allocation[ticker], target_allocation[ticker]))

        # TODO: Print remaining cash

        # Now that we're done, we can replace old portfolio with the new one
        self = balanced_portfolio 

    def _rebalance_objective_function(self, new_asset_values, current_asset_values, target_allocation):

        """
            Objective function used in optimization problem of portfolio rebalancing.

            Args:
                new_asset_values (np.ndarray): Market value of assets to buy.
                current_asset_vales (np.ndarray): Portfolio's current Market values of assets (in same currency as ``new_asset_values``).
                target_allocation: (np.ndarray): Target asset allocation (in %).

            Returns:
                float: Value of objective function.
        """

        # compute current allocation
        current_allocation = (current_asset_values + new_asset_values)/(np.sum(current_asset_values + new_asset_values))*100.      

        # Penalize asset allocation's far from target allocation (we use L2 norm)
        asset_alloc_diff = target_allocation - current_allocation
        j1 = np.inner(asset_alloc_diff, asset_alloc_diff)

        # Penalize unused cash (we use L2 norm)
        cash_diff = self._cash[Portfolio._common_currency].amount - np.sum(new_asset_values)
        j2 = 50.*np.inner(cash_diff, cash_diff)

        return j1 + j2

    def _sell_everything(self):

        """
            Sells all assets in the portfolio and converts them to cash. 
        """

        if Portfolio._common_currency not in self._cash.keys():
            self._cash[Portfolio._common_currency] = 0.00

        for asset in self._assets.values():
            self._cash[Portfolio._common_currency].amount += asset.market_value_in(Portfolio._common_currency)
            asset.quantity = 0
        
    def _buy_asset(self, ticker, quantity):
        """
            Buys the specified amount of an asset.

            Args:
                ticker (str): Ticker of asset to buy.
                quantity (int): Quantity to buy.
        """

        # TODO: first, attempt to buy using cash in asset's currency, then try other cash
        cost = self._assets[ticker].buy(quantity, currency=Portfolio._common_currency)
        self._cash[Portfolio._common_currency].amount -= cost