#!/usr/bin/env python
"""
Entrypoint da aplicação Flask para execução local e Vercel.

Se a aplicação principal falhar durante o boot, um app mínimo de diagnóstico
é exposto para que /health mostre a classe do erro sem vazar secrets.
"""
import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask, jsonify

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

BOOT_ERROR = None

try:
    from app.main import create_app
    app = create_app()
except Exception as exc:  # noqa: BLE001
    BOOT_ERROR = exc
    logging.exception("application_boot_failed")

    app = Flask(__name__)

    @app.get("/")
    @app.get("/health")
    @app.get("/health/ready")
    def boot_health():
        return jsonify({
            "status": "boot_failed",
            "service": "price-tracker",
            "error_type": type(BOOT_ERROR).__name__,
            "error": str(BOOT_ERROR),
        }), 503

    @app.errorhandler(404)
    def fallback_not_found(error):
        return jsonify({
            "status": "boot_failed",
            "error_type": type(BOOT_ERROR).__name__,
            "error": str(BOOT_ERROR),
        }), 503


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
