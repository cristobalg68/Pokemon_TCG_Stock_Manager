# Pokemon TCG Stock Manager

## Description

IPokemon TCG Stock Manager is a set of Python tools designed to help manage the inventory of a Pokémon TCG card store on the [TCGplayer](https://www.tcgplayer.com) platform. It automates stock updates, detects discrepancies between published and actual inventory, and suggests competitive prices based on competitor analysis. 

## Motivation

The main problem this project addresses is the difficulty of efficiently managing the stock of Pokémon TCG cards on TCGMatch. The challenges include:

* The platform interface does not display stock in a user-friendly way.

* Sales outside the platform do not automatically update the stock.

* Purchasing new cards requires manually verifying if existing listings exist.

To solve this, a system was developed based on an Excel database and Python scripts that perform web scraping to compare the actual stock with what is published on the platform.

## Features

* Centralized stock management: Easily view and update inventory.

* Synchronization with TCGMatch: Detect discrepancies between published and actual stock.

* Automated updates: Simplifies inventory updates after purchases or sales.

* Price analysis: Gathers competitor information and suggests competitive prices.

## Requirements

* Python 3.x

* Required libraries: 

    ![Pandas](https://img.shields.io/badge/Pandas-gray?style=flat&logo=Pandas) ![Numpy](https://img.shields.io/badge/Numpy-gray?style=flat&logo=Numpy) ![Selenium](https://img.shields.io/badge/Selenium-gray?style=flat&logo=Selenium) ![Requests](https://img.shields.io/badge/Requests-gray?style=flat&logo=Requests) ![Openpyxl](https://img.shields.io/badge/Openpyxl-gray?style=flat&logo=Openpyxl)

## Examples of use

~~~
Correct Publication Stock
-------------------------

Update Publication Stock
------------------------

Name: Dusclops / Card Type: Normal / Stock Quantity: 4 / Price Suggestion: English / Excellent / The minimum price within the RM is 350 / Outside the RM is 250

Name: Scream Tail / Card Type: Normal / Stock Quantity: 3 / Price Suggestion: English / Excellent / The minimum price within the RM is 150 / Outside the RM is 100

Name: Hippopotas / Card Type: Normal / Stock Quantity: 2 / Price Suggestion: English / Excellent / The minimum price within the RM is 298 / Outside the RM is 200

Name: Bloodmoon Ursaluna / Card Type: Holo / Stock Quantity: 2 / Price Suggestion: English / Excellent / The minimum price within the RM is 200 / Outside the RM is 300

Name: Houndour / Card Type: Normal / Stock Quantity: 2 / Price Suggestion: English / Excellent / The minimum price within the RM is 298 / Outside the RM is 200

Name: Bronzor / Card Type: Normal / Stock Quantity: 3 / Price Suggestion: English / Excellent / The minimum price within the RM is 298 / Outside the RM is 250

Create Publication
------------------

Name: Applin / Card Type: Normal / Stock Quantity: 1 / Price Suggestion: English / Excellent / The minimum price within the RM is 100 / Outside the RM is 100

Name: Pyroar / Card Type: Normal / Stock Quantity: 1 / Price Suggestion: English / Excellent / The minimum price within the RM is 150 / Outside the RM is 80

Name: Slowking / Card Type: Normal / Stock Quantity: 1 / Price Suggestion: English / Excellent / The minimum price within the RM is 500 / Outside the RM is 100

Name: Pupitar / Card Type: Normal / Stock Quantity: 2 / Price Suggestion: English / Excellent / The minimum price within the RM is 210 / Outside the RM is 200
~~~