import re
import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from app import db
from app.models import Store, Product, PriceChange

catalog_bp = Blueprint("catalog", __name__, url_prefix="/api")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _json():
    return request.get_json(silent=True) or {}


def _validate_common(data, fields):
    missing = [field for field in fields if data.get(field) in (None, "")]
    return f"Campos obrigatórios faltando: {', '.join(missing)}" if missing else None


@catalog_bp.get("/stores")
@jwt_required()
def list_stores():
    query = Store.query
    search = request.args.get("search", "").strip()
    if search:
        query = query.filter(or_(Store.name.ilike(f"%{search}%"), Store.email.ilike(f"%{search}%")))
    return jsonify([store.to_dict() for store in query.order_by(Store.name).all()])


@catalog_bp.post("/stores")
@jwt_required()
def create_store():
    data = _json()
    error = _validate_common(data, ["name", "email"])
    if error:
        return jsonify({"error": error}), 400
    if not EMAIL_RE.match(str(data["email"])):
        return jsonify({"error": "Email inválido"}), 400
    store = Store(id=str(uuid.uuid4()), name=str(data["name"]).strip(), email=str(data["email"]).strip().lower(), phone=data.get("phone"))
    db.session.add(store)
    db.session.commit()
    return jsonify({"data": store.to_dict()}), 201


@catalog_bp.get("/stores/<store_id>")
@jwt_required()
def get_store(store_id):
    store = db.session.get(Store, store_id)
    return jsonify(store.to_dict()) if store else (jsonify({"error": "Loja não encontrada"}), 404)


@catalog_bp.put("/stores/<store_id>")
@jwt_required()
def update_store(store_id):
    store = db.session.get(Store, store_id)
    if not store:
        return jsonify({"error": "Loja não encontrada"}), 404
    data = _json()
    if "name" in data and not str(data["name"]).strip():
        return jsonify({"error": "Nome é obrigatório"}), 400
    if "email" in data and not EMAIL_RE.match(str(data["email"])):
        return jsonify({"error": "Email inválido"}), 400
    for field in ("name", "email", "phone"):
        if field in data:
            setattr(store, field, str(data[field]).strip().lower() if field == "email" else data[field])
    db.session.commit()
    return jsonify({"data": store.to_dict()})


@catalog_bp.delete("/stores/<store_id>")
@jwt_required()
def delete_store(store_id):
    store = db.session.get(Store, store_id)
    if not store:
        return jsonify({"error": "Loja não encontrada"}), 404
    if store.products:
        return jsonify({"error": "Não é possível excluir uma loja com produtos"}), 409
    db.session.delete(store)
    db.session.commit()
    return jsonify({"message": "Loja excluída com sucesso"})


@catalog_bp.get("/products")
@jwt_required()
def list_products():
    query = Product.query
    search = request.args.get("search", "").strip()
    store_id = request.args.get("store_id")
    if search:
        query = query.filter(or_(Product.name.ilike(f"%{search}%"), Product.sku.ilike(f"%{search}%")))
    if store_id:
        query = query.filter_by(store_id=store_id)
    return jsonify([product.to_dict() for product in query.order_by(Product.name).all()])


@catalog_bp.post("/products")
@jwt_required()
def create_product():
    data = _json()
    error = _validate_common(data, ["store_id", "name", "sku", "current_price"])
    if error:
        return jsonify({"error": error}), 400
    store = db.session.get(Store, data["store_id"])
    if not store:
        return jsonify({"error": "Loja não encontrada"}), 404
    try:
        price = float(data["current_price"])
    except (TypeError, ValueError):
        return jsonify({"error": "Preço inválido"}), 400
    if price <= 0:
        return jsonify({"error": "Preço deve ser maior que zero"}), 400
    product = Product(id=str(uuid.uuid4()), store_id=store.id, name=str(data["name"]).strip(), sku=str(data["sku"]).strip(), current_price=price)
    db.session.add(product)
    db.session.commit()
    return jsonify({"data": product.to_dict()}), 201


@catalog_bp.get("/products/<product_id>")
@jwt_required()
def get_product(product_id):
    product = db.session.get(Product, product_id)
    return jsonify(product.to_dict()) if product else (jsonify({"error": "Produto não encontrado"}), 404)


@catalog_bp.get("/products/<product_id>/history")
@jwt_required()
def product_history(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(max(request.args.get("per_page", 20, type=int), 1), 100)
    pagination = PriceChange.query.filter_by(product_id=product_id).order_by(PriceChange.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({"product": product.to_dict(), "data": [item.to_dict() for item in pagination.items],
                    "total": pagination.total, "pages": pagination.pages, "page": page, "per_page": per_page})


@catalog_bp.put("/products/<product_id>")
@jwt_required()
def update_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    data = _json()
    if "current_price" in data:
        try:
            price = float(data["current_price"])
        except (TypeError, ValueError):
            return jsonify({"error": "Preço inválido"}), 400
        if price <= 0:
            return jsonify({"error": "Preço deve ser maior que zero"}), 400
        product.current_price = price
    for field in ("name", "sku"):
        if field in data and not str(data[field]).strip():
            return jsonify({"error": f"{field} é obrigatório"}), 400
        if field in data:
            setattr(product, field, str(data[field]).strip())
    db.session.commit()
    return jsonify({"data": product.to_dict()})


@catalog_bp.delete("/products/<product_id>")
@jwt_required()
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    if any(change.status in {"pending", "active"} for change in product.price_changes):
        return jsonify({"error": "Não é possível excluir produto com alterações abertas"}), 409
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Produto excluído com sucesso"})
