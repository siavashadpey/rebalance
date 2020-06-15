from rebalance import Portfolio, Asset, Cash

# My portfolio
p = Portfolio()

# Cash in portfolio
cash_amounts = [3000., 200.]
cash_currency = ["USD", "CAD"]
p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

# Assets in portfolio
# The price will be retrieved automatically
tickers = ["XBB.TO", "XIC.TO", "ITOT", "IEFA", "IEMG"]
quantities = [36, 64, 32, 8, 7]
p.easy_add_assets(tickers=tickers, quantities=quantities)

# Target asset allocation (in %)
target_asset_alloc = {
"XBB.TO": 20,
"XIC.TO": 20,
"ITOT":   36,
"IEFA":   20,
"IEMG":    4
}

# rebalance
p.selling_allowed = True # Don't allow selling while rebalancing
(new_units, prices, exchange_rates, max_diff) = p.rebalance(target_asset_alloc, verbose=True)