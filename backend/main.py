#!/usr/bin/env python
"""Entrypoint WSGI do Sistema Precificador para Vercel e execução local."""
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

from app.main import create_app

# A Vercel carrega este objeto via "main:app".
app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "5000")),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )
