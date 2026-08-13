from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
USERS = {
    "admin@pricetracker.com": {"password_hash": generate_password_hash("admin123"), "name": "Administrador"},
    "user@pricetracker.com": {"password_hash": generate_password_hash("user123"), "name": "Usuário"},
}


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email, password = data.get("email"), data.get("password")
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    user = USERS.get(str(email).lower())
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Email ou senha inválidos"}), 401
    token = create_access_token(identity=str(email).lower())
    return jsonify({"message": "Login realizado com sucesso", "token": token, "access_token": token,
                    "user": {"email": str(email).lower(), "name": user["name"]}})


@auth_bp.get("/me")
@jwt_required()
def get_me():
    email = get_jwt_identity()
    user = USERS.get(email)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify({"email": email, "name": user["name"]})


@auth_bp.post("/logout")
@jwt_required()
def logout():
    return jsonify({"message": "Logout realizado com sucesso"})
