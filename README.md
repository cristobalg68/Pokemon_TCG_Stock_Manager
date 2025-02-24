# Pokemon_TCG

In this repository you can find how to implement a simple Pokemon TCG card market research and a system to manage the stock of a small Pokemon TCG card store. 

The idea was, first of all, to create the dataset to know which cards I can sell, and then, to get the historical price (and other statistics) of a specific card in the market [TCGplayer](https://www.tcgplayer.com). 

The second step was to create the database with the actual stock I have and generate the release stock to compare the actual stock with the release stock and resolve any difference issues (more cards in stock to sell that have not been released or cards with no stock released). 

The final step was the creation of a pokemon card scanner to scan new cards and add all the new cards to the stock database to then compare the historical price of these cards so that these cards can be published in my local market [TCGmatch](https://tcgmatch.cl). It is important to mention that when I want to publish a new card, I need to update the historical price of the card and the stock of that card in my local market to know the supply and demand of that card.

To implement all of the above, I have used Python. For dataset creation and updating, I do web scraping which I implemented with the [add library/s] library. For database management I used the pandas and numpy libraries. For the creation of the pokemon card scanner I used a YOLO model and libraries like OpenCV and Pytorch.

## Problem

How can I know the price at which I can publish my pokemon cards in my local market and how can I manage the stock of pokemon cards to avoid having cards that have not been published or having cards published that I do not have in stock.

## Solution

