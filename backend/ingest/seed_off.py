"""
Seed the products table from Open Food Facts by category.

Usage (from backend/ directory):
  python -m ingest.seed_off --categories "beverages,snacks,canned-goods" --limit 200

For each product found, we fetch ingredients and run Claude scoring — so this
burns Anthropic API credits. Use --dry-run to preview without scoring.
"""

import argparse
import sys
import os

# Allow running from backend/ dir
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import requests
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from extensions import db
from models import Product
from routes.scan import score_with_claude
from datetime import datetime

OFF_SEARCH = (
    "https://world.openfoodfacts.org/cgi/search.pl"
    "?action=process&tagtype_0=categories&tag_contains_0=contains"
    "&tag_0={category}&fields=code,product_name,brands,ingredients_text_en,"
    "ingredients_text,image_front_url&json=1&page_size={page_size}&page={page}"
)


def fetch_category(category, limit):
    products = []
    page = 1
    while len(products) < limit:
        batch = min(50, limit - len(products))
        url = OFF_SEARCH.format(category=category, page_size=batch, page=page)
        try:
            r = requests.get(url, timeout=15)
            items = r.json().get("products", [])
        except Exception as e:
            print(f"  [warn] fetch failed for {category} page {page}: {e}")
            break
        if not items:
            break
        products.extend(items)
        page += 1
    return products[:limit]


def seed(categories, limit, dry_run):
    app = create_app()
    with app.app_context():
        total_new = 0
        for category in categories:
            print(f"\n── Category: {category} ──")
            items = fetch_category(category.strip(), limit)
            print(f"  Fetched {len(items)} products from Open Food Facts")

            for item in items:
                barcode = item.get("code", "").strip()
                if not barcode:
                    continue

                existing = Product.query.filter_by(barcode=barcode).first()
                if existing:
                    print(f"  [skip] {barcode} already in DB")
                    continue

                name = item.get("product_name") or ""
                ingredients = item.get("ingredients_text_en") or item.get("ingredients_text") or ""

                if not name or not ingredients:
                    print(f"  [skip] {barcode} — missing name or ingredients")
                    continue

                info = {
                    "name": name,
                    "brand": item.get("brands"),
                    "ingredients_raw": ingredients,
                    "image_url": item.get("image_front_url"),
                }

                print(f"  [score] {barcode} — {name[:50]}")

                if dry_run:
                    print(f"    (dry run — skipping Claude scoring)")
                    continue

                try:
                    scored = score_with_claude(info)
                except Exception as e:
                    print(f"    [error] scoring failed: {e}")
                    continue

                product = Product(
                    barcode=barcode,
                    name=info["name"],
                    brand=info["brand"],
                    ingredients_raw=info["ingredients_raw"],
                    image_url=info["image_url"],
                    plastic_percentage=scored["plastic_percentage"],
                    risk_summary=scored["risk_summary"],
                    risk_detail=scored["risk_detail"],
                    flagged_ingredients=scored["flagged_ingredients"],
                    cached_at=datetime.utcnow(),
                )
                db.session.add(product)
                db.session.commit()
                total_new += 1
                print(f"    → {scored['plastic_percentage']}% plastic — saved")

        print(f"\nDone. {total_new} new products seeded.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed products from Open Food Facts")
    parser.add_argument("--categories", required=True, help="Comma-separated OFF category tags")
    parser.add_argument("--limit", type=int, default=50, help="Max products per category")
    parser.add_argument("--dry-run", action="store_true", help="Fetch but don't score or save")
    args = parser.parse_args()

    cats = [c.strip() for c in args.categories.split(",") if c.strip()]
    seed(cats, args.limit, args.dry_run)
