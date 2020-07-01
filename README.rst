Rebalance
=========

|Build status| |Coverage| |Code Factor| |Docs| 

A calculator which tells you how to split your investment amongst your portfolio's assets based on your target asset allocation.

You can either install the package and write a driver file as described below or use the web-based calculator hosted on AWS `here <http://ec2-3-22-168-81.us-east-2.compute.amazonaws.com>`_.


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

    from rebalance import Portfolio

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
    cash_amounts = [3000., 200.]
    cash_currency = ["USD", "CAD"]
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

      Ticker      Ask     Quantity      Amount    Currency     Old allocation   New allocation     Target allocation
                           to buy         ($)                      (%)              (%)                 (%)
     ---------------------------------------------------------------------------------------------------------------
       XBB.TO    33.43       30         1002.90      CAD          17.52            19.99               20.00
       XIC.TO    24.27       27          655.29      CAD          22.61            20.01               20.00
         ITOT    69.38       10          693.80      USD          43.93            35.88               36.00
         IEFA    57.65       20         1153.00      USD           9.13            19.88               20.00
         IEMG    49.14        0            0.00      USD           6.81             4.24                4.00

     Largest discrepancy between the new and the target asset allocation is 0.24 %.

     Before making the above purchases, the following currency conversion is required:
         1072.88 USD to 1458.19 CAD at a rate of 1.3591.

     Remaining cash:
         80.32 USD.
         0.00 CAD.
	
.. raw:: html

        </div>



.. |Build Status| image:: https://travis-ci.org/siavashadpey/rebalance.svg?branch=master
	:target: https://travis-ci.org/siavashadpey/rebalance.svg?branch=master
	
.. |Coverage| image:: https://coveralls.io/repos/github/siavashadpey/rebalance/badge.svg?branch=master
	:target: https://coveralls.io/repos/github/siavashadpey/rebalance/badge.svg?branch=master

.. |Code Factor| image:: https://www.codefactor.io/repository/github/siavashadpey/rebalance/badge
   :target: https://www.codefactor.io/repository/github/siavashadpey/rebalance

.. |Docs| image:: https://readthedocs.org/projects/rebalance/badge/?version=latest
	:target: https://rebalance.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status
