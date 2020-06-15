from rebalance import Portfolio, Asset, Cash

# My portfolio
p = Portfolio()

# Cash in portfolio
cash_amounts = [500.]
cash_currency = ["CAD"]
p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

# Assets in portfolio
# The price will be retrieved automatically
tickers = ["VCN.TO", "XAW.TO", "ZAG.TO"]
quantities = [5, 12, 20]
p.easy_add_assets(tickers=tickers, quantities=quantities)

# Target asset allocation (in %)
target_asset_alloc = {
"VCN.TO": 40.0
"ZAG.TO": 40.0,
"XAW.TO": 20.0,
}

# rebalance
p.selling_allowed = True # Don't allow selling while rebalancing
(new_units, prices, exchange_rates, max_diff) = p.rebalance(target_asset_alloc, verbose=True)