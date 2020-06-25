from rebalance import Portfolio

p = Portfolio()

tickers = ["XBB.TO", "XIC.TO", "ITOT", "IEFA", "IEMG"]
quantities = [36, 64, 32, 8, 7]
p.easy_add_assets(tickers=tickers, quantities = quantities)
p.add_cash(5000.00, "GBP")
p.add_cash(1000.00, "EUR")

target_asset_alloc = {
"XBB.TO": 20,
"XIC.TO": 20,
"IEFA":   20,
"ITOT":   36,
"IEMG":    4
}


initial_value = p.value("CAD")
p.selling_allowed = False
(_, _, exchange_rates, _) = p.rebalance(target_asset_alloc, verbose=True)
final_value = p.value("CAD")
