from rebalance import Portfolio, Asset

# My portfolio
p = Portfolio()

# Cash in portfolio
cash_amounts = [3687]
cash_currency = ["USD"]
p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

# Assets in portfolio
# The price will be retrieved automatically
tickers = ["TSLA", "ITOT"]
quantities = [3, 10]
p.easy_add_assets(tickers=tickers, quantities=quantities)

# Target asset allocation (in %)
target_asset_alloc = {
"TSLA":   80,
"ITOT":   20
}

# rebalance
p.selling_allowed = True # Don't allow selling while rebalancing
p.rebalance(target_asset_alloc, verbose=True)