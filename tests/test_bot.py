import unittest
from supermarket_bot import SupermarketBot


class TestSupermarketBot(unittest.TestCase):
    def setUp(self):
        self.bot = SupermarketBot()

    def test_add_and_total(self):
        self.bot.add_item('apple', 1.0)
        self.bot.add_item('banana', 2.5)
        self.assertEqual(self.bot.total(), 3.5)

    def test_remove_item(self):
        self.bot.add_item('milk', 1.2)
        self.bot.remove_item('milk')
        self.assertEqual(self.bot.total(), 0)

    def test_remove_missing_item_raises(self):
        with self.assertRaises(KeyError):
            self.bot.remove_item('missing')

    def test_add_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self.bot.add_item('bad', -1)


if __name__ == '__main__':
    unittest.main()
