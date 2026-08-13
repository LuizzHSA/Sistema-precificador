from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Usuários simulados (em produção, seria do banco)
USERS = {
    'admin@pricetracker.com': {
        'password_hash': generate_password_hash('admin123'),
        'name': 'Administrador'
    },
    'user@pricetracker.com': {
        'password_hash': generate_password_hash('user123'),
        'name': 'Usuário'
    }
}

@auth_bp.route('/login', methods=['POST'])
def login():
    """Fazer login"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    user = USERS.get(email)
    
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Email ou senha inválidos'}), 401
    
    # Criar token JWT
    access_token = create_access_token(identity=email)
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': access_token,
        'user': {
            'email': email,
            'name': user['name']
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Obter dados do usuário autenticado"""
    email = get_jwt_identity()
    user = USERS.get(email)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'email': email,
        'name': user['name']
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Fazer logout"""
    # Em uma aplicação real, você adicionaria o token à blacklist
    return jsonify({'message': 'Logout realizado com sucesso'}), 200
