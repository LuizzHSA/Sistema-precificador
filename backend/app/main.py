from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

from app.config import config
from app import db, jwt
from app.routes.price_changes import price_bp
from app.routes.auth import auth_bp

load_dotenv()

def create_app(config_name=None):
    """Factory para criar a aplicação Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Carregar configurações
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(price_bp)
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok'}, 200
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("✓ Banco de dados inicializado")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
