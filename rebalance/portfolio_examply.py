from rebalance import Portfolio

# My portfolio
p = Portfolio()

# Assets in portfolio
# The price will be retrieved automatically
tickers = ["XBB.TO",   # iShares Core Canadian Universe Bond Index ETF
           "XIC.TO",   # iShares Core S&P/TSX Capped Composite Index ETF
           "ITOT",     # iShares Core S&P Total U.S. Stock Market ETF
           "IEFA",     # iShares Core MSCI EAFE ETF
           "IEMG"]     # iShares Core MSCI Emerging Markets ETF
quantities = [36, 64, 32, 8, 7]
p.easy_add_assets(tickers=tickers, quantities=quantities)

# Cash in portfolio
cash_amounts = [3000., 200.]
cash_currency = ["USD", "CAD"]
p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

# Target asset allocation (in %)
target_asset_alloc = {
"XBB.TO": 20,
"XIC.TO": 20,
"ITOT":   36,
"IEFA":   20,
"IEMG":    4
}

# rebalance
p.selling_allowed = False # We don't want to sell any of our assets for this case
p.rebalance(target_asset_alloc, verbose=True)
