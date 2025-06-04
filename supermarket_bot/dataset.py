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
    """Return category JSON or empty dict if the category does not exist."""
    try:
        return _get_json(f"/categories/{cat_id}/")
    except requests.HTTPError as exc:  # type: ignore[attr-defined]
        if exc.response is not None and exc.response.status_code == 404:
            return {}
        raise


def _root_categories() -> Iterable[int]:
    data = _get_json("/categories/")
    for cat in data.get("results", []):
        for sub in cat.get("categories", []):
            if isinstance(sub, dict) and "id" in sub:
                yield sub["id"]


def iter_products() -> Iterable[Dict]:
    """Yield all products available in the Mercadona API without duplicates."""
    cat_seen: Set[int] = set()
    product_seen: Set[int] = set()
    queue = list(_root_categories())
    while queue:
        cid = queue.pop()
        if cid in cat_seen:
            continue
        cat_seen.add(cid)
        cat = _fetch_category(cid)
        if not cat:
            continue
        for prod in cat.get("products", []):
            pid = prod.get("id")
            if pid not in product_seen:
                product_seen.add(pid)
                yield prod
        for sub in cat.get("categories", []):
            for prod in sub.get("products", []):
                pid = prod.get("id")
                if pid not in product_seen:
                    product_seen.add(pid)
                    yield prod
            if isinstance(sub, dict) and "id" in sub and sub["id"] not in cat_seen:
                queue.append(sub["id"])


def build_dataset(csv_path: str) -> None:
    """Fetch all products and write them to a CSV file with columns id, name and price."""
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
