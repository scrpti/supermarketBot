# supermarketBot

A simple command line supermarket assistant that lets you manage a small shopping cart. Use it to add or remove items and display the total amount.

## Installation

This project requires Python 3 and the dependencies listed in
`requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```

The dataset builder relies on the `requests` package which is included in
`requirements.txt`.

## Running the bot

```bash
python3 -m supermarket_bot
```

You will be presented with a menu to add items, remove items, list the cart contents and show the total price.

## Building a Mercadona product dataset

You can fetch all available products and prices from the public Mercadona API and
store them in a CSV file:

```bash
python3 -m supermarket_bot.dataset products.csv
```

## Running tests

```bash
python3 -m unittest
```
