import logging
import os
import time
from collections import defaultdict, deque
from flask import Flask, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.config import config
from app import db, jwt, migrate
from app.routes.auth import auth_bp
from app.routes.price_changes import price_bp
from app.routes.catalog import catalog_bp

load_dotenv()


def _production_config_issues(app):
    issues = []

    secret_key = app.config.get("SECRET_KEY") or ""
    jwt_secret = app.config.get("JWT_SECRET_KEY") or ""

    # Autenticação está temporariamente desativada para acesso direto.
    # Mantemos apenas a validação da infraestrutura necessária ao sistema.

    database_url = app.config.get("SQLALCHEMY_DATABASE_URI") or ""
    if not database_url or database_url.startswith("sqlite"):
        issues.append("DATABASE_URL")

    return issues


def create_app(config_name=None):
    config_name = config_name or os.getenv("FLASK_ENV", "development")
    instance_path = "/tmp/price-tracker-instance" if os.getenv("VERCEL") else None
    app = Flask(__name__, instance_path=instance_path) if instance_path else Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    logging.basicConfig(
        level=getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    config_issues = _production_config_issues(app) if config_name == "production" else []
    if config_issues:
        app.logger.error(
            "production_configuration_incomplete missing_or_invalid=%s",
            ",".join(config_issues),
        )

    app.config["PRODUCTION_CONFIG_ISSUES"] = config_issues

    request_hits = defaultdict(deque)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    @app.before_request
    def enforce_rate_limit():
        if request.path in ("/", "/health", "/health/ready"):
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

    @app.get("/")
    def root():
        return jsonify({
            "application": "Sistema Precificador",
            "status": "online",
            "service": "price-tracker",
            "api": "/api",
            "health": "/health",
            "readiness": "/health/ready",
            "metrics": "/metrics"
        }), 200

    @app.get("/health")
    def health():
        issues = app.config.get("PRODUCTION_CONFIG_ISSUES", [])
        if issues:
            return jsonify({
                "status": "degraded",
                "service": "price-tracker",
                "configuration": "incomplete",
                "missing_or_invalid": issues,
            }), 503
        return jsonify({
            "status": "ok",
            "service": "price-tracker",
            "configuration": "ok",
        }), 200

    @app.get("/health/ready")
    def readiness():
        issues = app.config.get("PRODUCTION_CONFIG_ISSUES", [])
        if issues:
            return jsonify({
                "status": "not_ready",
                "configuration": "incomplete",
                "missing_or_invalid": issues,
            }), 503

        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({
                "status": "ready",
                "database": "ok",
                "configuration": "ok",
            }), 200
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("readiness_check_failed")
            return jsonify({
                "status": "not_ready",
                "database": "error",
                "error": str(exc),
            }), 503

    @app.get("/metrics")
    def metrics():
        from app.models import Product, Store, PriceChange
        return jsonify({
            "stores_total": Store.query.count(),
            "products_total": Product.query.count(),
            "price_changes_total": PriceChange.query.count(),
            "price_changes_pending": PriceChange.query.filter_by(status="pending").count(),
            "price_changes_active": PriceChange.query.filter_by(status="active").count(),
            "price_changes_executed": PriceChange.query.filter_by(status="executed").count(),
        })

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
        try:
            db.session.rollback()
        except Exception:
            app.logger.exception("database_rollback_failed")

        app.logger.exception("unhandled_application_error")

        if app.config.get("TESTING"):
            raise error

        return jsonify({
            "error": "Erro interno do servidor",
            "type": type(error).__name__,
        }), 500

    with app.app_context():
        from app import models  # noqa: F401

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "5000")),
        debug=application.config["DEBUG"],
    )
