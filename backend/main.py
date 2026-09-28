#!/usr/bin/env python
"""
Entry point para a aplicação Flask.

Expõe `app` no nível do módulo para plataformas WSGI/Serverless
como a Vercel, mantendo a execução local via `python main.py`.
"""
import os
import sys
from dotenv import load_dotenv

# Adicionar diretório ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

load_dotenv()

from app.main import create_app

# Entrypoint WSGI usado pela Vercel: main:app
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"🚀 Iniciando servidor em http://localhost:{port}")
    print("📊 Dashboard: http://localhost:8080")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
