import unittest
from unittest import mock
import requests


from supermarket_bot import dataset

class TestDataset(unittest.TestCase):
    def test_iter_products(self):

        root_data = {"results": [{"categories": [{"id": 1}]}]}

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


    def test_iter_products_skips_missing_category(self):
        root_data = {"results": [{"categories": [{"id": 1}, {"id": 99}]}]}
        cat1_data = {"products": [{"id": "p1", "display_name": "Item1", "price_instructions": {"unit_price": "1.00"}}], "categories": []}

        def fake_get(url, *args, **kwargs):
            if url == f"{dataset.BASE_URL}/categories/":
                m = mock.Mock(); m.status_code = 200; m.json.return_value = root_data; return m
            if url == f"{dataset.BASE_URL}/categories/1/":
                m = mock.Mock(); m.status_code = 200; m.json.return_value = cat1_data; return m
            if url == f"{dataset.BASE_URL}/categories/99/":
                resp = mock.Mock(status_code=404)
                raise requests.HTTPError(response=resp)
            raise AssertionError(f"Unexpected URL: {url}")

        with mock.patch("supermarket_bot.dataset.requests.get", side_effect=fake_get):
            items = list(dataset.iter_products())

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], "p1")

    def test_iter_products_deduplicates(self):
        root_data = {"results": [{"categories": [{"id": 1}, {"id": 2}]}]}
        cat1_data = {"products": [{"id": "p1", "display_name": "Item1", "price_instructions": {"unit_price": "1.00"}}], "categories": []}
        cat2_data = {"products": [{"id": "p1", "display_name": "Item1Dup", "price_instructions": {"unit_price": "1.00"}}], "categories": []}

        responses = {
            f"{dataset.BASE_URL}/categories/": root_data,
            f"{dataset.BASE_URL}/categories/1/": cat1_data,
            f"{dataset.BASE_URL}/categories/2/": cat2_data,
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
