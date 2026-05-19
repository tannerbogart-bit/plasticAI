from extensions import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    ingredients_raw = db.Column(db.Text)
    image_url = db.Column(db.String(512))
    plastic_percentage = db.Column(db.Float)   # 0–100, the hero number shown to users
    confidence = db.Column(db.String(16))      # high / medium / low
    risk_summary = db.Column(db.Text)          # one-sentence plain-English verdict
    risk_detail = db.Column(db.Text)           # premium: full breakdown
    flagged_ingredients = db.Column(db.JSON)   # list of {name, percentage, reason, source, verified}
    cached_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, premium=False):
        data = {
            "barcode": self.barcode,
            "name": self.name,
            "brand": self.brand,
            "image_url": self.image_url,
            "plastic_percentage": self.plastic_percentage,
            "confidence": self.confidence,
            "risk_summary": self.risk_summary,
            "flagged_ingredients": (self.flagged_ingredients or [])[:3],  # top 3 free
        }
        if premium:
            data["flagged_ingredients"] = self.flagged_ingredients
            data["risk_detail"] = self.risk_detail
        return data


class Scan(db.Model):
    __tablename__ = "scans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scans = db.relationship("Scan", backref="user", lazy=True)
