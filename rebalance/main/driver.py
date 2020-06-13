from rebalance import Portfolio, Asset, Cash

# My portfolio
p = Portfolio()

# Cash in portfolio
cash_amounts = [500., 200.]
cash_currency = ["CAD", "USD"]
p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

# Assets in portfolio
# The price will be retrieved automatically
tickers = ["VCN.TO", "ZAG.TO", "XAW.TO"]
quantities = [5, 20, 12]
p.easy_add_assets(tickers=tickers, quantities=quantities)

# Current asset allocation (in %)
asset_alloc = p.asset_allocation()
print(asset_alloc)

# Check price and market value of an asset
print("The price of XAW.TO is " + str(p.assets["XAW.TO"].price) + " " + p.assets["XAW.TO"].currency)
print("My holdings of XAW.TO are valued at " + str(p.assets["XAW.TO"].market_value()) + " " + p.assets["XAW.TO"].currency)

# Target asset allocation (in %)
target_asset_alloc = {
"VCN.TO": 40.0,
"ZAG.TO": 40.0,
"XAW.TO": 20.0}

# rebalance
p.selling_allowed = False # Don't allow selling while rebalancing
p.rebalance(target_asset_alloc)
