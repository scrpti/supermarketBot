import csv
from typing import Iterable, Dict, Set
import requests

BASE_URL = "https://tienda.mercadona.es/api"


def _get_json(path: str) -> Dict:
    url = f"{BASE_URL}{path}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def _fetch_category(cat_id: int) -> Dict:
    return _get_json(f"/categories/{cat_id}/")


def _root_categories() -> Iterable[int]:
    data = _get_json("/categories/")
    for cat in data.get("results", []):
        yield cat["id"]


def iter_products() -> Iterable[Dict]:
    """Yield all products available in the Mercadona API."""
    seen: Set[int] = set()
    queue = list(_root_categories())
    while queue:
        cid = queue.pop()
        if cid in seen:
            continue
        seen.add(cid)
        cat = _fetch_category(cid)
        for prod in cat.get("products", []):
            yield prod
        for sub in cat.get("categories", []):
            for prod in sub.get("products", []):
                yield prod
            if isinstance(sub, dict) and "id" in sub and sub["id"] not in seen:
                queue.append(sub["id"])


def build_dataset(csv_path: str) -> None:
    """Fetch all products and write them to a CSV file."""
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "name", "price"])
        for prod in iter_products():
            price = prod.get("price_instructions", {}).get("unit_price")
            writer.writerow([prod.get("id"), prod.get("display_name"), price])


def main(argv: Iterable[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Mercadona product dataset")
    parser.add_argument("output", help="path to output CSV file")
    args = parser.parse_args(list(argv) if argv is not None else None)
    build_dataset(args.output)


if __name__ == "__main__":
    main()
