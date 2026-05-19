from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, origins=os.getenv("ALLOWED_ORIGINS", "*"))

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")

    db.init_app(app)

    from routes.scan import scan_bp
    from routes.auth import auth_bp

    app.register_blueprint(scan_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
