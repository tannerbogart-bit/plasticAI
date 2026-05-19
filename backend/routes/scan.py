from flask import Blueprint, jsonify, request
from extensions import db
from models import Product, Scan
from plastic_chemicals import get_reference_block
from datetime import datetime, timedelta
import requests
import anthropic
import json
import os

scan_bp = Blueprint("scan", __name__)

CACHE_TTL_DAYS = 7
OFF_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
UPC_URL = "https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"


def fetch_from_open_food_facts(barcode):
    try:
        r = requests.get(OFF_URL.format(barcode=barcode), timeout=8)
        data = r.json()
        if data.get("status") == 1:
            p = data["product"]
            return {
                "name": p.get("product_name") or p.get("product_name_en"),
                "brand": p.get("brands"),
                "ingredients_raw": p.get("ingredients_text_en") or p.get("ingredients_text"),
                "image_url": p.get("image_front_url"),
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
            }
    except Exception:
        pass
    return None


def score_with_claude(product_info):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    reference = get_reference_block()
    prompt = f"""You are a microplastics and synthetic chemical safety analyst. Your job is to estimate what percentage of a product's ingredients are plastic-derived, plastic-adjacent, or known to carry/leach microplastics.

Product: {product_info.get('name', 'Unknown')}
Brand: {product_info.get('brand', 'Unknown')}
Ingredients: {product_info.get('ingredients_raw', 'Not available')}

REFERENCE — known plastic-linked chemicals (use these to ground your analysis):
{reference}

Analyze each ingredient against this reference and estimate the overall plastic contamination percentage (0–100%). Also flag any other plastic-linked ingredients you know from research not in the list above.

Return ONLY valid JSON with this exact structure:
{{
  "plastic_percentage": <integer 0-100>,
  "risk_summary": "<one punchy sentence a consumer would immediately understand, e.g. 'Contains 3 ingredients linked to microplastic contamination'>",
  "risk_detail": "<2-3 paragraphs for premium users — which specific ingredients, what plastics they carry, what the health research says>",
  "flagged_ingredients": [
    {{"name": "<ingredient name>", "percentage": <estimated % contribution to plastic score>, "reason": "<one line why>"}}
  ]
}}

Be honest and calibrated. Most whole foods score 0-5%. Heavily processed foods with synthetic additives score 15-40%. Products with known plastic chemicals score 40-80%+."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
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
    # Check cache
    product = Product.query.filter_by(barcode=barcode).first()
    if product and product.cached_at > datetime.utcnow() - timedelta(days=CACHE_TTL_DAYS):
        premium = request.args.get("premium") == "true"
        return jsonify({"status": "ok", "product": product.to_dict(premium=premium)})

    # Fetch product info
    info = fetch_from_open_food_facts(barcode) or fetch_from_upc_itemdb(barcode)
    if not info or not info.get("name"):
        return jsonify({"status": "not_found", "message": "Product not found"}), 404

    # Score with Claude
    try:
        scored = score_with_claude(info)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Scoring failed: {str(e)}"}), 500

    # Upsert product
    if not product:
        product = Product(barcode=barcode)
        db.session.add(product)

    product.name = info["name"]
    product.brand = info["brand"]
    product.ingredients_raw = info["ingredients_raw"]
    product.image_url = info["image_url"]
    product.plastic_percentage = scored["plastic_percentage"]
    product.risk_summary = scored["risk_summary"]
    product.risk_detail = scored["risk_detail"]
    product.flagged_ingredients = scored["flagged_ingredients"]
    product.cached_at = datetime.utcnow()

    db.session.commit()

    premium = request.args.get("premium") == "true"
    return jsonify({"status": "ok", "product": product.to_dict(premium=premium)})
