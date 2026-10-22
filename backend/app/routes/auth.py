from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    config_issues = current_app.config.get("PRODUCTION_CONFIG_ISSUES", [])
    auth_issues = [
        item for item in config_issues
        if item in {"SECRET_KEY", "JWT_SECRET_KEY", "AUTH_EMAIL", "AUTH_PASSWORD_HASH"}
    ]
    if auth_issues:
        return jsonify({"error": "Configuração de autenticação incompleta"}), 503

    data = request.get_json(silent=True) or {}
    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    configured_email = str(current_app.config.get("AUTH_EMAIL") or "").strip().lower()
    password_hash = current_app.config.get("AUTH_PASSWORD_HASH")
    if not configured_email or not password_hash:
        return jsonify({"error": "Autenticação não configurada"}), 503

    try:
        password_ok = check_password_hash(password_hash, password)
    except (ValueError, TypeError):
        current_app.logger.error("AUTH_PASSWORD_HASH has an unsupported format")
        return jsonify({"error": "Configuração de autenticação inválida"}), 503

    if email != configured_email or not password_ok:
        return jsonify({"error": "Email ou senha inválidos"}), 401

    token = create_access_token(identity=email)
    return jsonify({
        "message": "Login realizado com sucesso",
        "token": token,
        "access_token": token,
        "user": {"email": email, "name": current_app.config.get("AUTH_NAME", "Administrador")},
    }), 200


@auth_bp.get("/me")
@jwt_required()
def get_me():
    email = get_jwt_identity()
    configured_email = str(current_app.config.get("AUTH_EMAIL") or "").strip().lower()
    if not configured_email or email != configured_email:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify({"email": email, "name": current_app.config.get("AUTH_NAME", "Administrador")})


@auth_bp.post("/logout")
@jwt_required()
def logout():
    # JWT access tokens are stateless. The client must discard its token.
    return jsonify({"message": "Logout realizado com sucesso"})
