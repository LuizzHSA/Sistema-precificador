import uuid
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User, Store, Product, PriceChange, ExecutionLog, AuditEvent

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
MIN_PASSWORD_LENGTH = 10


def issue_access_token(user):
    return create_access_token(
        identity=user.id,
        additional_claims={"token_version": user.token_version},
    )


def valid_email(email):
    if not email or len(email) > 255 or "@" not in email:
        return False
    if email.count("@") != 1:
        return False
    local, domain = email.split("@", 1)
    return bool(local and domain and "." in domain and not domain.startswith(".") and not domain.endswith("."))


def provision_configured_admin():
    email = str(current_app.config.get("AUTH_EMAIL") or "").strip().lower()
    password_hash = current_app.config.get("AUTH_PASSWORD_HASH")
    if not email or not password_hash:
        return None
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    user = User(id=str(uuid.uuid4()), name=current_app.config.get("AUTH_NAME", "Administrador"),
                email=email, password_hash=password_hash, is_admin=True, is_active=True)
    db.session.add(user)
    db.session.flush()
    # Existing records without an owner are retained under the configured legacy administrator.
    for model in (Store, Product, PriceChange, ExecutionLog, AuditEvent):
        model.query.filter_by(owner_id=None).update({model.owner_id: user.id}, synchronize_session=False)
    db.session.commit()
    return user


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name") or "").strip()
    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")
    if not name or len(name) > 120:
        return jsonify({"error": "Informe um nome válido (até 120 caracteres)"}), 400
    if not valid_email(email):
        return jsonify({"error": "E-mail inválido"}), 400
    configured_admin = str(current_app.config.get("AUTH_EMAIL") or "").strip().lower()
    if email == configured_admin:
        return jsonify({"error": "Este e-mail é reservado para a conta administrativa configurada"}), 409
    if len(password) < MIN_PASSWORD_LENGTH:
        return jsonify({"error": "A senha deve ter pelo menos 10 caracteres"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Já existe uma conta com este e-mail"}), 409
    user = User(id=str(uuid.uuid4()), name=name, email=email,
                password_hash=generate_password_hash(password), is_admin=False, is_active=True)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Já existe uma conta com este e-mail"}), 409
    token = issue_access_token(user)
    return jsonify({"message": "Conta criada com sucesso", "access_token": token, "token": token, "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")
    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400
    user = User.query.filter_by(email=email).first()
    if user is None and email == str(current_app.config.get("AUTH_EMAIL") or "").strip().lower():
        user = provision_configured_admin()
    if not user or not user.is_active:
        return jsonify({"error": "E-mail ou senha inválidos"}), 401
    try:
        password_ok = check_password_hash(user.password_hash, password)
    except (ValueError, TypeError):
        current_app.logger.error("Invalid stored password hash for user id=%s", user.id)
        return jsonify({"error": "Credenciais inválidas"}), 401
    if not password_ok:
        return jsonify({"error": "E-mail ou senha inválidos"}), 401
    token = issue_access_token(user)
    return jsonify({"message": "Login realizado com sucesso", "token": token,
                    "access_token": token, "user": user.to_dict()}), 200


@auth_bp.get("/me")
@jwt_required()
def get_me():
    user = db.session.get(User, str(get_jwt_identity()))
    if not user or not user.is_active:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(user.to_dict())


@auth_bp.post("/logout")
@jwt_required()
def logout():
    user = db.session.get(User, str(get_jwt_identity()))
    if not user or not user.is_active:
        return jsonify({"error": "Usuário não encontrado"}), 404
    # Invalidate all previously issued tokens for this account, including the current one.
    user.token_version += 1
    db.session.commit()
    return jsonify({"message": "Logout realizado com sucesso"})
