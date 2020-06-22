import copy
import math
from typing import Sequence

import numpy as np
from scipy.optimize import minimize

from rebalance import Asset
from rebalance import Cash
from rebalance import Price


class Portfolio:
    """
    Portfolio class.

    Defines a :class:`.Portfolio` of :class:`.Asset` s and :class:`.Cash` and performs rebalancing of the portfolio.

    """
    def __init__(self):
        """
        Initialization.
        """
        self._assets = {}
        self._cash = {}
        self._is_selling_allowed = False
        self._common_currency = "CAD"

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

        if currency.upper() not in self._cash.keys():
            self._cash[currency.upper()] = Cash(amount, currency)
        else:
            self._cash[currency.upper()].amount += amount

    def easy_add_cash(self, amounts, currencies):
        """
        An easy way of adding cash of various currencies to portfolio.

        Args:
            amounts (Sequence[float]): Amounts of cash from different curriencies.
            currencies (Sequence[str]): Specifies curriency of each of the amounts. Must be  in the same order as ``amounts``.

        """
        assert len(amounts) == len(
            currencies
        ), "`amounts` and `currencies` should be of the same length."
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
        total_value = self.market_value(self._common_currency)

        total_value = max(
            1., total_value
        )  # protect against division by 0 (total_value = 0, means new portfolio)

        asset_allocation = {}
        for name, asset in self._assets.items():
            asset_allocation[name] = asset.market_value_in(
                self._common_currency) / total_value * 100.

        return asset_allocation

    def market_value(self, currency):
        """
        Computes the total market value of the assets in the portfolio.

        Args:
            currency (str): The currency in which to obtain the value.

        Returns:
            float: The total market value of the assets in the portfolio.
        """

        mv = 0.
        for asset in self.assets.values():
            mv += asset.market_value_in(currency)

        return mv

    def cash_value(self, currency):
        """
        Computes the cash value in the portfolio.

        Args:
            currency (str): The currency in which to obtain the value.

        Returns:
            float: The total cash value in the portfolio.
        """

        cv = 0.
        for cash in self.cash.values():
            cv += cash.amount_in(currency)

        return cv

    def value(self, currency):
        """
        Computes the total value (cash and assets) in the portfolio.

        Args:
            currency (str): The currency in which to obtain the value.

        Returns:
            float: The total value in the portfolio.
        """

        return self.market_value(currency) + self.cash_value(currency)

    def rebalance(self, target_allocation, verbose=False):
        """
            Rebalances the portfolio using the specified target allocation, the portfolio's current allocation,
            and the available cash.

            Args:
                target_allocation (Dict[str, float]): Target asset allocation of the portfolio (in %). The keys of the dictionary are the tickers of the assets.
                verbose (bool, optional): Verbosity flag. Default is False. 

            Returns:
                (tuple): tuple containing:
                    * new_units (Dict[str, int]): Units of each asset to buy. The keys of the dictionary are the tickers of the assets.
                    * prices (Dict[str, [float, str]]): The keys of the dictionary are the tickers of the assets. Each value of the dictionary is a 2-entry list. The first entry is the price of the asset during the rebalancing computation. The second entry is the currency of the asset.
                    * exchange_rates (Dict[str, float]): The keys of the dictionary are currencies. Each value is the exchange rate to CAD during the rebalancing computation.
                    * max_diff (float): Largest difference between target allocation and optimized asset allocation.
        """

        # order target_allocation dict in the same order as assets dict and upper key
        target_allocation_reordered = {}
        try:
            for key in self._assets.keys():
                target_allocation_reordered[key] = target_allocation[key]
        except:
            raise Exception(
                "'target_allocation not compatible with the assets of the portfolio."
            )

        target_allocation_np = np.fromiter(
            target_allocation_reordered.values(), dtype=float)

        assert abs(np.sum(target_allocation_np) -
                   100.) <= 1E-2, "target allocation must sum up to 100%."

        # Set common currency
        self._common_currency = next(iter(
            self._cash))  # first currency in cash dict

        # Make a new instance of portfolio
        # This is the one that is going to be rebalanced
        # We do not modify the current portfolio
        balanced_portfolio = copy.deepcopy(self)

        # If selling is allowed, "sell everything" in new portfolio
        if self.selling_allowed:
            balanced_portfolio._sell_everything()

        # Convert all cash to one currency
        total_cash = 0.
        for cash in balanced_portfolio.cash.values():
            total_cash += cash.amount_in(self._common_currency)
        balanced_portfolio.cash = {
            self._common_currency:
            Cash(total_cash, balanced_portfolio._common_currency)
        }

        # Solve optimization problem
        nb_assets = len(balanced_portfolio._assets)
        bound = (0.00, total_cash)
        bounds = ((bound, ) * nb_assets)
        constraints = [{
            'type':
            'ineq',
            'fun':
            lambda new_asset_values: balanced_portfolio.cash[
                self._common_currency].amount - np.sum(new_asset_values)
        }]  # Can't buy more than available cash
        current_asset_values = np.array([
            asset.market_value_in(self._common_currency)
            for asset in balanced_portfolio.assets.values()
        ])
        new_asset_values0 = target_allocation_np / 100. * balanced_portfolio.value(
            self._common_currency) - current_asset_values

        solution = minimize(balanced_portfolio._rebalance_objective_function,
                            new_asset_values0,
                            args=(current_asset_values,
                                  target_allocation_np / 100.),
                            method='SLSQP',
                            bounds=bounds,
                            constraints=constraints)

        # See how many units of each asset you need to buy based on optimization solution
        # and total cost/currency
        new_units = {}
        currency_cost = {}
        for sol_mv, ticker in zip(solution.x,
                                  balanced_portfolio.assets.keys()):
            if self.selling_allowed:
                # first buy original assets, then see how much you need to buy or sell extra
                # this method discourages selling when optimizer finds a solution very close to original holding
                # (e.g. optimizer: buy 4.8 --> rounds to 4, original = 5)
                new_units[ticker] = int(
                    (sol_mv - self.assets[ticker].market_value_in(
                        self._common_currency)) / self.assets[ticker].price_in(
                            self._common_currency))  # round towards 0
            else:
                new_units[ticker] = int(
                    sol_mv /
                    self.assets[ticker].price_in(self._common_currency))

            asset_i = self.assets[ticker]
            if asset_i.currency not in currency_cost.keys():
                currency_cost[asset_i.currency] = asset_i.cost_of(
                    new_units[ticker])
            else:
                currency_cost[asset_i.currency] += asset_i.cost_of(
                    new_units[ticker])

        # Since we converted the cash to one commeon currency for the rebalancing calculation, revert back
        balanced_portfolio.cash = copy.deepcopy(self.cash)

        # Since we might have sold all assets for the rebalancing calculation, revert back
        balanced_portfolio._assets = copy.deepcopy(self.assets)

        # Make necessary currency conversions
        exchange_history = balanced_portfolio._smart_exchange(currency_cost)

        # Buy new units
        prices = {}
        cost = {}
        for ticker, asset in balanced_portfolio.assets.items():
            prices[ticker] = [asset.price,
                              asset.currency]  # price and currency of price
            cost[ticker] = balanced_portfolio.buy_asset(
                ticker, new_units[ticker])

        # compute old and new asset allocation
        # and largest diff between new and target asset allocation
        old_alloc = self.asset_allocation()
        new_alloc = balanced_portfolio.asset_allocation()
        max_diff = max(
            abs(target_allocation_np -
                np.fromiter(new_alloc.values(), dtype=float)))

        if verbose:
            print("")
            # Print shares to buy, cost, new allocation, old allocation target, and target allocation
            print(
                " Ticker      Ask     Quantity      Amount    Currency     Old allocation   New allocation     Target allocation"
            )
            print(
                "                      to buy         ($)                      (%)              (%)                 (%)"
            )
            print(
                "---------------------------------------------------------------------------------------------------------------"
            )
            for ticker in balanced_portfolio.assets.keys():
                print("%8s  %7.2f   %6.d        %8.2f     %4s          %5.2f            %5.2f               %5.2f" % \
                (ticker, prices[ticker][0], new_units[ticker], cost[ticker], prices[ticker][1], old_alloc[ticker], new_alloc[ticker], target_allocation[ticker]))

            print("")
            print(
                "Largest discrepancy between the new and the target asset allocation is %.2f %%."
                % (max_diff))

            # Print conversion exchange
            if len(exchange_history) > 0:
                print("")
                if len(exchange_history) > 1:
                    print(
                        "Before making the above purchases, the following currency conversions are required:"
                    )
                else:
                    print(
                        "Before making the above purchases, the following currency conversion is required:"
                    )

                for exchange in exchange_history:
                    (from_amount, from_currency, to_amount, to_currency,
                     rate) = exchange
                    print("    %.2f %s to %.2f %s at a rate of %.4f." %
                          (from_amount, from_currency, to_amount, to_currency,
                           rate))

            # Print remaining cash
            print("")
            #print("Remaining cash: %.2f %s." % (balanced_portfolio.cash[self._common_currency].amount, self._common_currency))
            print("Remaining cash:")
            for cash in balanced_portfolio.cash.values():
                print("    %.2f %s." % (cash.amount, cash.currency))

        # Now that we're done, we can replace old portfolio with the new one
        self.__dict__.update(balanced_portfolio.__dict__)

        return (new_units, prices, exchange_history, max_diff)

    def _rebalance_objective_function(self, new_asset_values,
                                      current_asset_values, target_allocation):
        """
            Objective function used in optimization problem of portfolio rebalancing.

            Args:
                new_asset_values (np.ndarray): Market value of assets to buy.
                current_asset_vales (np.ndarray): Portfolio's current Market values of assets (in same currency as ``new_asset_values``).
                target_allocation: (np.ndarray): Target asset allocation (in decimal).

            Returns:
                float: Value of objective function.
        """

        # total asset value
        asset_vals = current_asset_values + new_asset_values
        tot_asset_val = np.sum(asset_vals)
        # compute current allocation
        current_allocation = asset_vals / tot_asset_val

        # Penalize asset allocation's far from target allocation (we use L2 norm)
        asset_alloc_diff = target_allocation - current_allocation
        j1 = np.inner(asset_alloc_diff, asset_alloc_diff)  # range: (0, 1)

        # Penalize unused cash (we use L2 norm)
        cash_diff = (self._cash[self._common_currency].amount -
                     np.sum(new_asset_values)) / (
                         self._cash[self._common_currency].amount +
                         np.sum(new_asset_values))
        j2 = cash_diff * cash_diff  # range: (0, 1)

        return j1 + j2

    def _sell_everything(self):
        """
            Sells all assets in the portfolio and converts them to cash. 
        """

        for ticker, asset in self._assets.items():
            self.buy_asset(ticker, - asset.quantity)

    def buy_asset(self, ticker, quantity):
        """
        Buys (or sells) the specified amount of an asset.

        Args:
            ticker (str): Ticker of asset to buy.
            quantity (int): If positive, it is the quantity to buy. If negative, it is the quantity to sell.

        Return:
            float: Cost of transaction (in asset's own currency)
        """
        if quantity == 0:
            return 0.00

        asset = self.assets[ticker]
        cost = asset.buy(quantity)
        self.add_cash(-cost, asset.currency)
        return cost

    def _smart_exchange(self, currency_amount):
        """
        Performs currency exchange between Portfolio's different sources of cash based on amount required per currency.

        Args:
            currency_amount (Dict[str, float]): Amount needed per currency. The keys of the dictionary are the currency.
    
        Returns:
            List[tuple]: tuple containing:
                    *  from_amount (float): Amount exchanged from currency indicated by `from_currency`
                    *  from_currency (str): Currency from which to perform the exchange
                    *  to_amount (float): Amount exchanged to currency indicated by `to_currency`
                    *  to_currency (str): Currency to which to perform the exchange
                    *  rate (float): Currency exchange rate from `from_currency` to `to_currency`
        """

        # first, compute amount we have to convert to and amount we have for conversion
        

        to_conv = {}
        from_conv = copy.deepcopy(self.cash)
        for curr in currency_amount.keys():
            if curr not in self.cash.keys():
                from_conv[curr] = Cash(0.00, curr)

            to = currency_amount[curr] - from_conv[curr].amount

            if to > 0:
                to_conv[curr] = Cash(to, curr)
                del from_conv[curr]  # no extra cash available for conversion
            else:
                # no conversion will be necessary
                from_conv[curr].amount -= currency_amount[curr]

        # perform currency exchange
        exchange_history = []
        for to_cash in to_conv.values():
            one_exchange = False
            # Try converting one shot if possible
            for from_cash in from_conv.values():
                if from_cash.amount_in(to_cash.currency) >= to_cash.amount:
                    # perform conversion
                    self.exchange_currency(to_currency=to_cash.currency,
                                           from_currency=from_cash.currency,
                                           to_amount=to_cash.amount)

                    # update amount we have to convert to or amount we have for conversion
                    amt = to_cash.amount_in(from_cash.currency)

                    rate = from_cash.exchange_rate(to_cash.currency)
                    exchange_history.append(
                        (amt, from_cash.currency, to_cash.amount,
                         to_cash.currency, rate))

                    from_cash.amount -= amt
                    to_cash.amount = 0.00

                    # move to next 'to_cash'
                    one_exchange = True
                    break

            # If we reached here,
            # it means we couldn't perform one currency exchange to meet our 'to_cash'
            # So we'll just convert whatever we can
            if not one_exchange:
                for from_cash in from_conv.values():
                    if from_cash.amount_in(to_cash.currency) >= to_cash.amount:
                        # perform conversion
                        self.exchange_currency(
                            to_currency=to_cash.currency,
                            from_currency=from_cash.currency,
                            to_amount=to_cash.amount)

                        amt = to_cash.amount_in(from_cash.currency)
                        rate = from_cash.exchange_rate(to_cash.currency)
                        exchange_history.append(
                            (amt, from_cash.currency, to_cash.amount,
                             to_cash.currency, rate))

                        # update amount we have to convert to and amount we have for conversion
                        from_cash.amount -= amt
                        to_cash.amount = 0.00
                    else:
                        self.exchange_currency(
                            to_currency=to_cash.currency,
                            from_currency=from_cash.currency,
                            from_amount=from_cash.amount)
                        amt = from_cash.amount_in(to_cash.currency)

                        rate = from_cash.exchange_rate(to_cash.currency)
                        exchange_history.append(
                            (from_cash.amount, from_cash.currency, amt,
                             to_cash.currency, rate))

                        # update amount we have to convert to and amount we have for conversion
                        to_cash.amount -= amt
                        from_cash.amount = 0.00

        return exchange_history

    def exchange_currency(self,
                          to_currency,
                          from_currency,
                          to_amount=None,
                          from_amount=None):
        """
        Performs currency exchange in Portfolio.

        Args:
            to_currency (str): Currency to which to perform the exchange
            from_currency (str): Currency from which to perform the exchange
            to_amount (float, optional): If specified, it is the amount to which we want to convert
            from_amount (float, optional): If specified, it is the amount from which we want to convert

        Note: either the `to_amount` or `from_amount` needs to be specifed.
        """

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # add cash instances of both currencies to portfolio if non-existent
        self.add_cash(0.0, from_currency)
        self.add_cash(0.0, to_currency)

        if to_amount is None and from_amount is None:
            raise Exception(
                "Argument `to_amount` or `from_amount` must be specified.")
        elif to_amount is not None and from_amount is not None:
            raise Exception(
                "Please specify only `to_amount` or `from_amount`, not both.")
        elif to_amount is not None:
            from_amount = self.cash[to_currency].exchange_rate(
                from_currency) * to_amount
        elif from_amount is not None:
            to_amount = self.cash[from_currency].exchange_rate(
                to_currency) * from_amount

        self.add_cash(to_amount, to_currency)
        self.add_cash(-from_amount, from_currency)
