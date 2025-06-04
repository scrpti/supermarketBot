# supermarketBot

A simple command line supermarket assistant that lets you manage a small shopping cart. Use it to add or remove items and display the total amount.

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
