from flask import Blueprint, jsonify, request
from extensions import db
from models import Product, Scan
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

    prompt = f"""You are a microplastics safety analyst. Analyze this product's ingredients and return a JSON risk assessment.

Product: {product_info.get('name', 'Unknown')}
Brand: {product_info.get('brand', 'Unknown')}
Ingredients: {product_info.get('ingredients_raw', 'Not available')}

Return ONLY valid JSON with this exact structure:
{{
  "risk_score": <float 0.0-10.0>,
  "risk_summary": "<one sentence for free tier users>",
  "risk_detail": "<2-3 paragraphs for premium users explaining plastic chemicals found, exposure risks, and why>",
  "flagged_ingredients": [
    {{"name": "<ingredient>", "risk": "<low|medium|high>", "reason": "<brief explanation>"}}
  ]
}}

Risk score guide: 0-3 = low risk, 4-6 = moderate, 7-10 = high risk.
Flag ingredients like: microplastics, BPA, phthalates, PFAS, polystyrene, PVC, artificial dyes with plastic carriers, synthetic preservatives linked to plastics."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
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
    product.risk_score = scored["risk_score"]
    product.risk_summary = scored["risk_summary"]
    product.risk_detail = scored["risk_detail"]
    product.flagged_ingredients = scored["flagged_ingredients"]
    product.cached_at = datetime.utcnow()

    db.session.commit()

    premium = request.args.get("premium") == "true"
    return jsonify({"status": "ok", "product": product.to_dict(premium=premium)})
