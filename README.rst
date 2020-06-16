Rebalance
=========

|Build status| |Coverage| |Docs|

A calculator which tells you how to split your investment amongst your portfolio's assets based on your target asset allocation.

.. raw:: html

        <div class="ui container">

        <h2 class="ui dividing header">Installation</h2>

                <div class="ui text container">
.. raw:: html

                    <h3 class="ui header">Clone the repository:</h3>

.. code-block:: bash

    git clone https://github.com/siavashadpey/rebalance.git

.. raw:: html

                    <h3 class="ui header">Install the package:</h3>

.. code-block:: bash

    cd rebalance
    pip3 install .

.. raw:: html

                    <h3 class="ui header">Run the unit tests to see if package was successfully installed:</h3>

.. code-block:: bash

    make test

.. raw:: html

            </div>
        </div>


        <div class="ui container">

        <h2 class="ui dividing header">Example</h2>


                    <h3 class="ui header">Make a driver file:</h3>

                    <p> The driver file is where we create our portfolio. We specify all of its assets and the available cash we have to invest. </p>

.. code-block:: bash

    cd rebalance
    touch driver_file.py

.. raw:: html

                    <h3 class="ui header">Import all necessary packages:</h3>

.. code-block:: python

    from rebalance import Portfolio, Asset

.. raw:: html

                    <h3 class="ui header">First we create our portfolio:</h3>

.. code-block:: python

    # My portfolio
    p = Portfolio()

.. raw:: html

                    <h3 class="ui header">Then we add our assets:</h3>
                    <p> We must specify the ticker symbol and the quantity of each asset we currently have in our portfolio.</p>
		    <p></p>
		    <i>The portfolio used in this example is one of 
		    	<a href="https://www.canadianportfoliomanagerblog.com/model-etf-portfolios/">
		    	Canadian Portfolio Manager</a>'s model portfolios. This blog along with 
		    	<a href="https://canadiancouchpotato.com/getting-started/">Canadian Couch Potato</a>
			advocate low-cost, globally diversified index funds for DIY investors. </i>

.. code-block:: python

    # Assets in portfolio
    # The price will be retrieved automatically
    tickers = ["XBB.TO",   # iShares Core Canadian Universe Bond Index ETF
    	       "XIC.TO",   # iShares Core S&P/TSX Capped Composite Index ETF
	       "ITOT",     # iShares Core S&P Total U.S. Stock Market ETF
	       "IEFA",     # iShares Core MSCI EAFE ETF
	       "IEMG"]     # iShares Core MSCI Emerging Markets ETF
    quantities = [36, 64, 32, 8, 7]
    p.easy_add_assets(tickers=tickers, quantities=quantities)

.. raw:: html

                    <h3 class="ui header">We also need to add cash to our portfolio: </h3>
                    <p> This is the amount that we are investing. We can add cash in different currencies.</p>

.. code-block:: python

    # Cash in portfolio
    cash_amounts = [500., 200.]
    cash_currency = ["CAD", "USD"]
    p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

.. raw:: html

                    <h3 class="ui header">Finally, we need to specify our target asset allocation:</h3>
		    <i> The target asset allocation used in this example is that of an
		         aggressive portfolio with 80% equities and 20% bonds (XBB.TO). </i>

.. code-block:: python

    # Target asset allocation (in %)
    target_asset_alloc = {
    "XBB.TO": 20,
    "XIC.TO": 20,
    "ITOT":   36,
    "IEFA":   20,
    "IEMG":    4
    }

.. raw:: html

                    <h3 class="ui header">Let the optimizer rebalance our portfolio!</h3>

.. code-block:: python

    # rebalance
    p.selling_allowed = False # We don't want to sell any of our assets for this case
    p.rebalance(target_asset_alloc, verbose=True)

.. raw:: html

                    <p>You should see something similar to this (the actual values might differ due to changes in prices and exchange rates).</p>

.. code-block:: bash

     Ticker    Ask     Quantity      Amount    Currency     Old allocation   New allocation     Target allocation
                        to buy         ($)                      (%)              (%)                 (%)
    -------------------------------------------------------------------------------------------------------------
      XBB.TO  33.43       29          969.47      CAD          17.89            19.97                20.00
      XIC.TO  24.16       27          652.32      CAD          22.99            20.21                20.00
        ITOT  67.35       11          740.85      USD          43.51            36.14                36.00
        IEFA  56.19       20         1123.80      USD           9.07            19.63                20.00
        IEMG  46.23        0            0.00      USD           6.53             4.04                 4.00
    
    Remaining cash: 119.63 CAD.
    Largest discrepancy between the new and the target asset allocation is 0.37 %.
    
    The exchange rate from USD to CAD is 1.3577.


.. raw:: html

        </div>



.. |Build Status| image:: https://travis-ci.org/siavashadpey/rebalance.svg?branch=master
	:target: https://travis-ci.org/siavashadpey/rebalance.svg?branch=master
	
.. |Coverage| image:: https://coveralls.io/repos/github/siavashadpey/rebalance/badge.svg?branch=master
	:target: https://coveralls.io/repos/github/siavashadpey/rebalance/badge.svg?branch=master

.. |Docs| image:: https://readthedocs.org/projects/rebalance/badge/?version=latest
	:target: https://rebalance.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status
