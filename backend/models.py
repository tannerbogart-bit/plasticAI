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
    risk_score = db.Column(db.Float)          # 0.0 (clean) – 10.0 (high risk)
    risk_summary = db.Column(db.Text)
    risk_detail = db.Column(db.Text)          # premium field
    flagged_ingredients = db.Column(db.JSON)  # list of {name, risk, reason}
    cached_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, premium=False):
        data = {
            "barcode": self.barcode,
            "name": self.name,
            "brand": self.brand,
            "image_url": self.image_url,
            "risk_score": self.risk_score,
            "risk_summary": self.risk_summary,
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
