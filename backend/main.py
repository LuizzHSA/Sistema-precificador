#!/usr/bin/env python
"""
Entry point para a aplicação Flask
"""
import os
import sys
from dotenv import load_dotenv

# Adicionar diretório ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

load_dotenv()

from app.main import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Iniciando servidor em http://localhost:{port}")
    print(f"📊 Dashboard: http://localhost:8080")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
