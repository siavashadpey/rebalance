from rebalance import Portfolio

# My portfolio
p = Portfolio()

# Cash in portfolio
cash_amounts = [5000]
cash_currency = ["CAD"]
p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

# Assets in portfolio
# The price will be retrieved automatically
tickers = ["XIC.TO", "VCN.TO", "TSLA"]
quantities = [20, 20, 10]
p.easy_add_assets(tickers=tickers, quantities=quantities)

# Target asset allocation (in %)
target_asset_alloc = {
 "XIC.TO": 20,
 "VCN.TO": 30,
 "TSLA":   50
}

# rebalance
p.selling_allowed = True # Don't allow selling while rebalancing
p.rebalance(target_asset_alloc, verbose=True)