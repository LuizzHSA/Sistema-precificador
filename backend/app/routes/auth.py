from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    config_issues = current_app.config.get("PRODUCTION_CONFIG_ISSUES", [])
    if config_issues:
        return jsonify({
            "error": "Configuração de produção incompleta",
            "missing_or_invalid": config_issues,
        }), 503

    data = request.get_json(silent=True) or {}
    email, password = data.get("email"), data.get("password")

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    configured_email = current_app.config.get("AUTH_EMAIL")
    password_hash = current_app.config.get("AUTH_PASSWORD_HASH")
    normalized_email = str(email).strip().lower()

    try:
        password_ok = check_password_hash(password_hash, password)
    except (ValueError, TypeError):
        current_app.logger.exception("invalid_auth_password_hash")
        return jsonify({
            "error": "AUTH_PASSWORD_HASH inválido na configuração do servidor"
        }), 503

    if normalized_email != configured_email.lower() or not password_ok:
        return jsonify({"error": "Email ou senha inválidos"}), 401

    token = create_access_token(identity=normalized_email)
    return jsonify({
        "message": "Login realizado com sucesso",
        "token": token,
        "access_token": token,
        "user": {
            "email": normalized_email,
            "name": current_app.config["AUTH_NAME"],
        },
    })


@auth_bp.get("/me")
@jwt_required()
def get_me():
    email = get_jwt_identity()
    if not current_app.config.get("AUTH_EMAIL") or email != current_app.config["AUTH_EMAIL"].lower():
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify({"email": email, "name": current_app.config["AUTH_NAME"]})


@auth_bp.post("/logout")
@jwt_required()
def logout():
    return jsonify({"message": "Logout realizado com sucesso"})
