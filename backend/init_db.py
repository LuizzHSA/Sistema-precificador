#!/usr/bin/env python
"""
Inicializa o banco de dados e cria todas as tabelas
"""
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

from app.main import create_app
from app import db

def init_db():
    """Cria todas as tabelas no banco de dados"""
    app = create_app()
    
    with app.app_context():
        print("🗄️  Inicializando banco de dados...")
        db.create_all()
        print("✅ Banco de dados inicializado com sucesso!")
        print(f"📍 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    init_db()
