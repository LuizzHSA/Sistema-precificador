#!/usr/bin/env python
"""Entrypoint WSGI do Sistema Precificador para Vercel."""

import json
import logging
import os
import sys
import traceback

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logger = logging.getLogger(__name__)
BOOT_ERROR = None
FLASK_APP = None

try:
    from dotenv import load_dotenv
    load_dotenv()

    from app.main import create_app
    FLASK_APP = create_app()
except Exception as exc:  # noqa: BLE001
    logger.exception("price_tracker_application_boot_failed")
    BOOT_ERROR = {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(limit=8),
    }


def app(environ, start_response):
    """Handler WSGI exportado explicitamente para a Vercel via main:app."""
    if FLASK_APP is not None:
        return FLASK_APP(environ, start_response)

    # Detailed diagnostics are kept in server logs, never exposed to clients.
    payload = json.dumps(
        {
            "status": "boot_failed",
            "service": "price-tracker",
            "error": "Falha ao iniciar a API. Consulte os logs do servidor.",
        },
        ensure_ascii=False,
    ).encode("utf-8")

    start_response(
        "503 Service Unavailable",
        [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(payload))),
            ("Cache-Control", "no-store"),
        ],
    )
    return [payload]


if __name__ == "__main__":
    if BOOT_ERROR:
        print(json.dumps(BOOT_ERROR, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    FLASK_APP.run(
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "5000")),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )
