import logging
import os
import time
from collections import defaultdict, deque
from flask import Flask, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import inspect, text
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
    if config_name == "production" and (app.config["SECRET_KEY"].startswith("dev-") or app.config["JWT_SECRET_KEY"].startswith("jwt-secret")):
        raise RuntimeError("Segredos de produção devem ser definidos por variáveis de ambiente")
    logging.basicConfig(level=getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO), format="%(asctime)s %(levelname)s %(name)s %(message)s")
    request_hits = defaultdict(deque)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    @app.before_request
    def enforce_rate_limit():
        if request.path == "/health" or request.path == "/health/ready":
            return None
        now = time.monotonic()
        bucket = request_hits[request.remote_addr or "unknown"]
        while bucket and now - bucket[0] > app.config["RATE_WINDOW_SECONDS"]:
            bucket.popleft()
        if len(bucket) >= app.config["RATE_LIMIT"]:
            return jsonify({"error": "Limite de requisições excedido"}), 429
        bucket.append(now)
        return None

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'")
        if config_name == "production":
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        return response

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(price_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "price-tracker"}), 200

    @app.get("/health/ready")
    def readiness():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "ready", "database": "ok"}), 200
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("readiness_check_failed")
            return jsonify({"status": "not_ready", "database": "error", "error": str(exc)}), 503

    @app.get("/metrics")
    def metrics():
        from app.models import Product, Store, PriceChange
        return jsonify({"stores_total": Store.query.count(), "products_total": Product.query.count(),
                        "price_changes_total": PriceChange.query.count(),
                        "price_changes_pending": PriceChange.query.filter_by(status="pending").count(),
                        "price_changes_active": PriceChange.query.filter_by(status="active").count(),
                        "price_changes_executed": PriceChange.query.filter_by(status="executed").count()})

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Requisição inválida"}), 400

    @app.errorhandler(RequestEntityTooLarge)
    def payload_too_large(error):
        return jsonify({"error": "Payload excede o limite permitido"}), 413

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
        columns = {column["name"] for column in inspect(db.engine).get_columns("price_changes")}
        if "retry_count" not in columns:
            db.session.execute(text("ALTER TABLE price_changes ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0"))
            db.session.commit()
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=int(os.getenv("API_PORT", "5000")), debug=application.config["DEBUG"])
