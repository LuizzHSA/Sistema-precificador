from functools import wraps

from flask import current_app, jsonify, request


def handle_errors(f):
    """Converte falhas inesperadas em respostas seguras e registra detalhes apenas no servidor."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:  # noqa: BLE001
            current_app.logger.exception("unhandled_route_error", extra={"route": request.path})
            return jsonify({"error": "Erro interno do servidor"}), 500
    return decorated_function


def require_json(f):
    """Rejeita requisições que não enviam um corpo JSON."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type deve ser application/json"}), 400
        return f(*args, **kwargs)
    return decorated_function
