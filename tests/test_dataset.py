import unittest
from unittest import mock

from supermarket_bot import dataset

class TestDataset(unittest.TestCase):
    def test_iter_products(self):
        root_data = {"results": [{"id": 1}]}
        cat1_data = {
            "products": [],
            "categories": [
                {
                    "id": 2,
                    "products": [
                        {
                            "id": "p1",
                            "display_name": "Item1",
                            "price_instructions": {"unit_price": "1.00"},
                        }
                    ],
                }
            ],
        }
        responses = {
            f"{dataset.BASE_URL}/categories/": root_data,
            f"{dataset.BASE_URL}/categories/1/": cat1_data,
            f"{dataset.BASE_URL}/categories/2/": {"products": []},
        }

        def fake_get(url, *args, **kwargs):
            data = responses.get(url)
            if data is None:
                raise AssertionError(f"Unexpected URL: {url}")
            m = mock.Mock()
            m.status_code = 200
            m.json.return_value = data
            return m

        with mock.patch("supermarket_bot.dataset.requests.get", side_effect=fake_get):
            items = list(dataset.iter_products())
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], "p1")

if __name__ == "__main__":
    unittest.main()
