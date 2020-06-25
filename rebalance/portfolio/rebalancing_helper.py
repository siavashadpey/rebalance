import copy
import math

import numpy as np
from scipy.optimize import minimize

def rebalance(portfolio, target_allocation):
    """
    Rebalances the portfolio using the specified target allocation, the portfolio's current allocation,
    and the available cash.

    Args:
        portfolio (:class:`.Portfolio`): Object of portfolio to rebalance.
        target_allocation (Dict[str, float]): Target asset allocation of the portfolio (in %). The keys of the dictionary are the tickers of the assets.

    Returns:
        (tuple): tuple containing:
            * new_units (Dict[str, int]): Units of each asset to buy. The keys of the dictionary are the tickers of the assets.
            * prices (Dict[str, [float, str]]): The keys of the dictionary are the tickers of the assets. Each value of the dictionary is a 2-entry list. The first entry is the price of the asset during the rebalancing computation. The second entry is the currency of the asset.
            * cost (Dict[str, float]): Market value of each asset to buy. The keys of the dictionary are the tickers of the assets.
            * exchange_rates (Dict[str, float]): The keys of the dictionary are currencies. Each value is the exchange rate to CAD during the rebalancing computation.
    """

    # Make a new instance of portfolio
    # This is the one that is going to be rebalanced
    # We do not modify the current portfolio
    balanced_portfolio = copy.deepcopy(portfolio)

    # If selling is allowed, "sell everything" in new portfolio
    if portfolio.selling_allowed:
        balanced_portfolio._sell_everything()

    # Convert all cash to one currency
    balanced_portfolio._combine_cash()
    
    # Solve optimization problem
    to_buy_vals = rebalance_optimizer(balanced_portfolio, target_allocation)
    
    # See how many units of each asset you need to buy based on optimization solution
    # and total cost/currency
    cmn_curr = portfolio._common_currency
    new_units = {}
    currency_cost = {}
    for sol_mv, ticker in zip(to_buy_vals,
                              balanced_portfolio.assets.keys()):
        if portfolio.selling_allowed:
            new_units[ticker] = math.floor(
                (sol_mv - portfolio.assets[ticker].market_value_in(
                    cmn_curr)) / portfolio.assets[ticker].price_in(
                        cmn_curr))
        else:
            new_units[ticker] = math.floor(
                sol_mv /
                portfolio.assets[ticker].price_in(cmn_curr))

        asset_i = portfolio.assets[ticker]
        if asset_i.currency not in currency_cost:
            currency_cost[asset_i.currency] = asset_i.cost_of(
                new_units[ticker])
        else:
            currency_cost[asset_i.currency] += asset_i.cost_of(
                new_units[ticker])

    # Since we converted the cash to one common currency for the rebalancing calculation, revert back
    balanced_portfolio.cash = copy.deepcopy(portfolio.cash)

    # Since we might have sold all assets for the rebalancing calculation, revert back
    balanced_portfolio._assets = copy.deepcopy(portfolio.assets)

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


    return balanced_portfolio, new_units, prices, cost, exchange_history


def rebalance_optimizer(portfolio, target_alloc):
    """
    Handles the optimization algorithm for the rebalancing procedure

    Args:
        portfolio (:class:`.Portfolio`): Object of portfolio to rebalance.
        target_alloc (np.ndarray): Target allocation of Portfolio's assets (in %).

    Returns:
        (np.ndarray): Optimizer's solution, which is the total market value of each asset to purchase.
    """

    cmn_curr = portfolio._common_currency
    nb_assets = len(portfolio.assets)
    total_cash = portfolio.cash[cmn_curr].amount
    bound = (0.00, total_cash)
    bounds = ((bound, ) * nb_assets)
    constraints = [{
        'type':
        'ineq',
        'fun':
        lambda new_asset_values: total_cash - np.sum(new_asset_values)
    }]  # Can't buy more than available cash

    current_asset_values = np.array([
        asset.market_value_in(cmn_curr)
        for asset in portfolio.assets.values()
    ])
    new_asset_values0 = target_alloc / 100. * portfolio.value(
        cmn_curr) - current_asset_values

    solution = minimize(rebalance_objective,
                        new_asset_values0,
                        args=(current_asset_values,
                              target_alloc / 100., 
                              total_cash),
                        method='SLSQP',
                        bounds=bounds,
                        constraints=constraints)

    return solution.x

def rebalance_objective(new_asset_values, current_asset_values, 
                         target_allocation, total_cash):
    """
    Objective function used in optimization problem of portfolio rebalancing.

    Args:
        new_asset_values (np.ndarray): Market value of assets to buy.
        current_asset_vales (np.ndarray): Portfolio's current Market values of assets (in same currency as ``new_asset_values``).
        target_allocation (np.ndarray): Target asset allocation (in decimal).
        total_cash (float): Total cash available for investing.

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
    cash_diff = (total_cash -
                 np.sum(new_asset_values)) / (
                     total_cash +
                     np.sum(new_asset_values))
    j2 = cash_diff * cash_diff  # range: (0, 1)

    return j1 + j2