from functools import wraps
from flask import jsonify

def handle_errors(f):
    """Decorator para tratamento de erros"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return decorated_function

def require_json(f):
    """Decorator para requisições JSON"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function
