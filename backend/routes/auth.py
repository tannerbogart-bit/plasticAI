from flask import Blueprint, jsonify, request, session
from extensions import db
from models import User, Scan, Product
import hashlib
import os

auth_bp = Blueprint("auth", __name__)


def hash_password(password):
    salt = os.getenv("SECRET_KEY", "dev")
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(email=email, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()
    session["user_id"] = user.id
    return jsonify({"status": "ok", "user": {"id": user.id, "email": user.email, "is_premium": user.is_premium}})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email, password_hash=hash_password(password)).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user.id
    return jsonify({"status": "ok", "user": {"id": user.id, "email": user.email, "is_premium": user.is_premium}})


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "ok"})


@auth_bp.route("/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"user": None})
    user = User.query.get(user_id)
    if not user:
        return jsonify({"user": None})
    return jsonify({"user": {"id": user.id, "email": user.email, "is_premium": user.is_premium}})


@auth_bp.route("/history")
def history():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    rows = (
        db.session.query(Scan, Product)
        .join(Product, Scan.product_id == Product.id)
        .filter(Scan.user_id == user_id)
        .order_by(Scan.scanned_at.desc())
        .limit(100)
        .all()
    )

    scans = [
        {
            "scan_id": scan.id,
            "scanned_at": scan.scanned_at.isoformat(),
            "barcode": product.barcode,
            "name": product.name,
            "brand": product.brand,
            "image_url": product.image_url,
            "plastic_percentage": product.plastic_percentage,
            "risk_summary": product.risk_summary,
        }
        for scan, product in rows
    ]
    return jsonify({"scans": scans})
