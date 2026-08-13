import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from app.config import config
from app import db, jwt
from app.routes.auth import auth_bp
from app.routes.price_changes import price_bp
from app.routes.catalog import catalog_bp

load_dotenv()


def create_app(config_name=None):
    config_name = config_name or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(price_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "price-tracker"}), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        db.session.rollback()
        return jsonify({"error": "Registro duplicado ou relacionado a dados existentes"}), 409

    @app.errorhandler(Exception)
    def internal_error(error):
        db.session.rollback()
        if app.config.get("TESTING"):
            raise error
        return jsonify({"error": "Erro interno do servidor"}), 500

    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=int(os.getenv("API_PORT", "5000")), debug=application.config["DEBUG"])
