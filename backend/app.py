from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db, migrate
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, origins=os.getenv("ALLOWED_ORIGINS", "*"), supports_credentials=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.getenv("FLASK_ENV") == "production"

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from routes.scan import scan_bp
    from routes.auth import auth_bp

    app.register_blueprint(scan_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
