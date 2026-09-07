#!/usr/bin/env python
"""Aplica as migrations do banco de dados."""
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

from app.main import create_app
from flask_migrate import upgrade

def init_db():
    """Atualiza o banco até a última revisão disponível."""
    app = create_app()
    
    with app.app_context():
        print("Aplicando migrations do banco de dados...")
        upgrade(directory=os.path.join(os.path.dirname(__file__), "migrations"))
        print("Banco de dados atualizado com sucesso!")
        print(f"📍 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    init_db()
