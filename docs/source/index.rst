.. rebalance documentation master file, created by
   sphinx-quickstart on Fri Jun 12 10:13:42 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. title:: rebalance's Documentation

Welcome to rebalance's documentation!
=====================================

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

    ./run_all_tests.sh

.. raw:: html

            </div>
        </div>


        <div class="ui container">

        <h2 class="ui dividing header">Example</h2>


                    <h3 class="ui header">Make a driver file:</h3>

                    <p> The driver file is where we create our portfolio. We specify all of its assets and the available cash. </p>

.. code-block:: bash

    cd rebalance
    touch driver_file.py

.. raw:: html

                    <h3 class="ui header">Import all necessary packages:</h3>

.. code-block:: python

    from rebalance import Portfolio, Asset, Cash

.. raw:: html

                    <h3 class="ui header">Instantiate a portfolio:</h3>

.. code-block:: python

    # My portfolio
    p = Portfolio()

.. raw:: html

                    <h3 class="ui header">Add cash to our portfolio. </h3>
                    <p> The amount and the currency must be specified.</p>

.. code-block:: python

    # Cash in portfolio
    cash_amounts = [500., 200.]
    cash_currency = ["CAD", "USD"]
    p.easy_add_cash(amounts=cash_amounts, currencies=cash_currency)

.. raw:: html

                    <h3 class="ui header">Specify the assets in our portfolio.</h3>
                    <p> The ticker symbol and quantity of the assets must be specified.</p>

.. code-block:: python

    # Assets in portfolio
    # The price will be retrieved automatically
    tickers = ["VCN.TO", "ZAG.TO", "XAW.TO"]
    quantities = [5, 20, 12]
    p.easy_add_assets(tickers=tickers, quantities=quantities)


.. raw:: html

                    <h3 class="ui header">We can check our current asset allocation:</h3>

.. code-block:: python

    # Current asset allocation (in %)
    asset_alloc = p.asset_allocation()
    print(asset_alloc)

.. raw:: html

                    <p>You should see something similar to this (the actual values might differ due to price changes).</p>

.. code-block:: bash

    {'VCN.TO': 19.268951399080024,
     'ZAG.TO': 40.96733219055606,
     'XAW.TO': 39.76371641036392}

.. raw:: html

                    <h3 class="ui header">We can also check other things such as the price and the market value of any asset:</h3>

.. code-block:: python

    print("The price of XAW.TO is " + str(p.assets["XAW.TO"].price) + " " + p.assets["XAW.TO"].currency)
    print("My holdings of XAW.TO are valued at " + str(p.assets["XAW.TO"].market_value()) + " " + p.assets["XAW.TO"].currency)


.. raw:: html

                    <p>You should see something similar to this (the actual values might differ due to price changes).</p>

.. code-block:: bash

    The price of XAW.TO is 26.87 CAD
    My holdings of XAW.TO are valued at 322.44 CAD

.. raw:: html

                    <h3 class="ui header">Once we're done investigating, we need to specify our target asset allocation.</h3>

.. code-block:: python

    # Target asset allocation (in %)
    target_asset_alloc = {
    "VCN.TO": 40.0,
    "ZAG.TO": 40.0,
    "XAW.TO": 20.0}

.. raw:: html

                    <h3 class="ui header">Let the optimizer rebalance our portfolio!</h3>

.. code-block:: python

    # rebalance
    p.selling_allowed = False # To allow or not to allow selling while rebalancing
    p.rebalance(target_asset_alloc)

.. raw:: html

                    <p>You should see something similar to this (the actual values might differ due to price changes).</p>

.. code-block:: bash

    Ticker     Quantity   Amount   Currency   Old allocation   New allocation   Target allocation
                to buy      ($)                    (%)              (%)                (%)
    ----------------------------------------------------------------------------------------------
    VCN.TO       15        468.75    CAD            19               40                 40
    ZAG.TO       17        282.37    CAD            41               39                 40
    XAW.TO        0          0.00    CAD            40               21                 20


.. raw:: html

        </div>

