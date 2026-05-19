from flask import Blueprint, jsonify, request, session
from extensions import db
from models import Product, Scan
from plastic_chemicals import get_reference_block, match_ingredients
from packaging_profiles import get_packaging_block, get_packaging_profile
from additives import get_additives_block, match_additives
from datetime import datetime, timedelta
import requests
import anthropic
import json
import os

scan_bp = Blueprint("scan", __name__)

CACHE_TTL_DAYS = 7
OFF_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json?fields=product_name,product_name_en,brands,ingredients_text_en,ingredients_text,image_front_url,categories_tags,packaging_tags,additives_tags"
UPC_URL = "https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"


def fetch_from_open_food_facts(barcode):
    try:
        r = requests.get(OFF_URL.format(barcode=barcode), timeout=8)
        data = r.json()
        if data.get("status") == 1:
            p = data["product"]
            return {
                "name": p.get("product_name_en") or p.get("product_name"),
                "brand": p.get("brands"),
                "ingredients_raw": p.get("ingredients_text_en") or p.get("ingredients_text"),
                "image_url": p.get("image_front_url"),
                "categories_tags": p.get("categories_tags", []),
                "packaging_tags": p.get("packaging_tags", []),
                "additives_tags": p.get("additives_tags", []),
            }
    except Exception:
        pass
    return None


def fetch_from_upc_itemdb(barcode):
    try:
        r = requests.get(UPC_URL.format(barcode=barcode), timeout=8)
        data = r.json()
        items = data.get("items", [])
        if items:
            item = items[0]
            return {
                "name": item.get("title"),
                "brand": item.get("brand"),
                "ingredients_raw": item.get("description"),
                "image_url": (item.get("images") or [None])[0],
                "categories_tags": [],
                "packaging_tags": [],
                "additives_tags": [],
            }
    except Exception:
        pass
    return None


def score_with_claude(product_info):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Pre-screen with our reference databases
    pre_matched = match_ingredients(product_info.get("ingredients_raw", ""))
    packaging_block = get_packaging_block(
        product_info.get("packaging_tags"),
        product_info.get("categories_tags"),
    )
    additives_block = get_additives_block(product_info.get("additives_tags"))
    reference_block = get_reference_block()

    # Build confidence hint based on data richness
    has_ingredients = bool(product_info.get("ingredients_raw"))
    has_packaging = bool(packaging_block)
    has_additives = bool(additives_block)
    data_richness = "rich" if (has_ingredients and (has_packaging or has_additives)) else ("partial" if has_ingredients else "minimal")

    pre_matched_block = ""
    if pre_matched:
        lines = [f"  - {m['name']}: +{m['pct']}% — {m['reason']}" for m in pre_matched[:10]]
        pre_matched_block = "PRE-MATCHED (confirmed in ingredients):\n" + "\n".join(lines)

    prompt = f"""You are a microplastics safety analyst. Estimate the plastic contamination percentage for this product.

Product: {product_info.get('name', 'Unknown')}
Brand: {product_info.get('brand', 'Unknown')}
Ingredients: {product_info.get('ingredients_raw') or 'Not available'}
Data richness: {data_richness}

{pre_matched_block}

{packaging_block}

{additives_block}

REFERENCE DATABASE (all known plastic-linked chemicals):
{reference_block}

Instructions:
1. Start from the pre-matched chemicals above (they are confirmed present)
2. Factor in packaging risk if listed
3. Factor in flagged additives if listed
4. Use the reference database to catch anything else
5. Calibrate: whole foods = 0-5%, processed foods = 5-20%, highly synthetic = 20-50%, direct plastic chemicals = 50%+

Return ONLY valid JSON:
{{
  "plastic_percentage": <integer 0-100>,
  "confidence": "<high|medium|low>",
  "risk_summary": "<one punchy sentence — e.g. 'Contains 2 phthalates and is packaged in BPA-lined cans'>",
  "risk_detail": "<2-3 paragraphs for premium: specific chemicals, health research, exposure context>",
  "flagged_ingredients": [
    {{
      "name": "<chemical or ingredient name>",
      "percentage": <its contribution to the plastic score>,
      "reason": "<one line>",
      "source": "<ingredient|packaging|additive>",
      "verified": <true if matched against reference DB, false if inferred by Claude>
    }}
  ]
}}

Set confidence=high if ingredients were available and ≥1 chemical was pre-matched.
Set confidence=medium if ingredients were available but no pre-matches.
Set confidence=low if no ingredient data was available."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


@scan_bp.route("/scan/<barcode>")
def scan(barcode):
    # Serve from cache if fresh
    product = Product.query.filter_by(barcode=barcode).first()
    if product and product.cached_at > datetime.utcnow() - timedelta(days=CACHE_TTL_DAYS):
        user_id = session.get("user_id")
        if user_id:
            db.session.add(Scan(user_id=user_id, product_id=product.id))
            db.session.commit()
        premium = request.args.get("premium") == "true"
        return jsonify({"status": "ok", "product": product.to_dict(premium=premium)})

    # Fetch product data
    info = fetch_from_open_food_facts(barcode) or fetch_from_upc_itemdb(barcode)
    if not info or not info.get("name"):
        return jsonify({"status": "not_found", "message": "Product not found"}), 404

    # Score
    try:
        scored = score_with_claude(info)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Scoring failed: {str(e)}"}), 500

    # Upsert
    if not product:
        product = Product(barcode=barcode)
        db.session.add(product)

    product.name = info["name"]
    product.brand = info["brand"]
    product.ingredients_raw = info["ingredients_raw"]
    product.image_url = info["image_url"]
    product.plastic_percentage = scored["plastic_percentage"]
    product.confidence = scored.get("confidence", "medium")
    product.risk_summary = scored["risk_summary"]
    product.risk_detail = scored["risk_detail"]
    product.flagged_ingredients = scored["flagged_ingredients"]
    product.cached_at = datetime.utcnow()

    db.session.commit()

    # Record scan in history for logged-in users
    user_id = session.get("user_id")
    if user_id:
        db.session.add(Scan(user_id=user_id, product_id=product.id))
        db.session.commit()

    premium = request.args.get("premium") == "true"
    return jsonify({"status": "ok", "product": product.to_dict(premium=premium)})
