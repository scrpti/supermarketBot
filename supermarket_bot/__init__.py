__all__ = ["SupermarketBot"]

class SupermarketBot:
    """A simple in-memory shopping cart."""

    def __init__(self):
        self.items = {}

    def add_item(self, name, price):
        if price < 0:
            raise ValueError("price can't be negative")
        self.items[name] = price

    def remove_item(self, name):
        if name not in self.items:
            raise KeyError(name)
        del self.items[name]

    def total(self):
        return sum(self.items.values())

    def list_items(self):
        return list(self.items.items())


def main():
    bot = SupermarketBot()
    menu = (
        "\n1) Add item\n" "2) Remove item\n" "3) Show total\n" "4) List items\n" "5) Exit\n"
    )
    while True:
        choice = input(menu + "Select an option: ")
        if choice == "1":
            name = input("Item name: ")
            price = float(input("Price: "))
            try:
                bot.add_item(name, price)
                print(f"Added {name} for {price:.2f}")
            except ValueError as exc:
                print(exc)
        elif choice == "2":
            name = input("Item name to remove: ")
            try:
                bot.remove_item(name)
                print(f"Removed {name}")
            except KeyError:
                print("Item not found")
        elif choice == "3":
            print(f"Total: {bot.total():.2f}")
        elif choice == "4":
            for name, price in bot.list_items():
                print(f"{name}: {price:.2f}")
        elif choice == "5":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
