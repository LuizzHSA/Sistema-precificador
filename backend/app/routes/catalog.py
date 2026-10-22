import math
import re
import uuid
from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from app import db
from app.models import Store, Product, PriceChange

catalog_bp = Blueprint("catalog", __name__, url_prefix="/api")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _json(): return request.get_json(silent=True) or {}
def _validate_common(data, fields):
    missing = [field for field in fields if data.get(field) in (None, "")]
    return f"Campos obrigatórios faltando: {', '.join(missing)}" if missing else None

@catalog_bp.get("/stores")
def list_stores():
    query = Store.query; search = request.args.get("search", "").strip()
    if search: query = query.filter(or_(Store.name.ilike(f"%{search}%"), Store.email.ilike(f"%{search}%")))
    return jsonify([store.to_dict() for store in query.order_by(Store.name).all()])

@catalog_bp.post("/stores")
def create_store():
    data = _json(); error = _validate_common(data, ["name", "email"])
    if error: return jsonify({"error": error}), 400
    if not EMAIL_RE.match(str(data["email"])): return jsonify({"error": "Email inválido"}), 400
    name = str(data["name"]).strip()
    email = str(data["email"]).strip().lower()
    phone = str(data.get("phone") or "").strip() or None
    if not name or len(name) > 120:
        return jsonify({"error": "Nome da loja deve ter entre 1 e 120 caracteres"}), 400
    if len(email) > 255:
        return jsonify({"error": "Email deve ter até 255 caracteres"}), 400
    if phone and len(phone) > 40:
        return jsonify({"error": "Telefone deve ter até 40 caracteres"}), 400
    store = Store(id=str(uuid.uuid4()), name=name, email=email, phone=phone)
    db.session.add(store)
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
            return jsonify({"error": "Já existe uma loja com este email"}), 409
        raise
    return jsonify({"data": store.to_dict()}), 201

@catalog_bp.get("/stores/<store_id>")
def get_store(store_id):
    store = db.session.get(Store, store_id); return jsonify(store.to_dict()) if store else (jsonify({"error": "Loja não encontrada"}), 404)

@catalog_bp.put("/stores/<store_id>")
def update_store(store_id):
    store = db.session.get(Store, store_id)
    if not store: return jsonify({"error": "Loja não encontrada"}), 404
    data = _json()
    if "name" in data and (not str(data["name"]).strip() or len(str(data["name"]).strip()) > 120):
        return jsonify({"error": "Nome deve ter entre 1 e 120 caracteres"}), 400
    if "email" in data and (not EMAIL_RE.match(str(data["email"]).strip()) or len(str(data["email"]).strip()) > 255):
        return jsonify({"error": "Email inválido"}), 400
    if "phone" in data and len(str(data["phone"] or "").strip()) > 40:
        return jsonify({"error": "Telefone deve ter até 40 caracteres"}), 400
    for field in ("name", "email", "phone"):
        if field in data:
            value = str(data[field] or "").strip()
            if field == "email":
                value = value.lower()
            elif field == "phone":
                value = value or None
            setattr(store, field, value)
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
            return jsonify({"error": "Já existe uma loja com este email"}), 409
        raise
    return jsonify({"data": store.to_dict()})

@catalog_bp.delete("/stores/<store_id>")
def delete_store(store_id):
    store = db.session.get(Store, store_id)
    if not store: return jsonify({"error": "Loja não encontrada"}), 404
    if store.products: return jsonify({"error": "Não é possível excluir uma loja com produtos"}), 409
    db.session.delete(store); db.session.commit(); return jsonify({"message": "Loja excluída com sucesso"})

@catalog_bp.get("/products")
def list_products():
    query = Product.query; search = request.args.get("search", "").strip(); store_id = request.args.get("store_id")
    if search: query = query.filter(or_(Product.name.ilike(f"%{search}%"), Product.sku.ilike(f"%{search}%")))
    if store_id: query = query.filter_by(store_id=store_id)
    return jsonify([product.to_dict() for product in query.order_by(Product.name).all()])

@catalog_bp.post("/products")
def create_product():
    data = _json(); error = _validate_common(data, ["store_id", "name", "sku", "current_price"])
    if error: return jsonify({"error": error}), 400
    store = db.session.get(Store, data["store_id"])
    if not store: return jsonify({"error": "Loja não encontrada"}), 404
    try: price = float(data["current_price"])
    except (TypeError, ValueError): return jsonify({"error": "Preço inválido"}), 400
    if not math.isfinite(price): return jsonify({"error": "Preço deve ser um número finito"}), 400
    if price <= 0: return jsonify({"error": "Preço deve ser maior que zero"}), 400
    name, sku = str(data["name"]).strip(), str(data["sku"]).strip()
    if not name or len(name) > 160: return jsonify({"error": "Nome do produto deve ter entre 1 e 160 caracteres"}), 400
    if not sku or len(sku) > 80: return jsonify({"error": "SKU deve ter entre 1 e 80 caracteres"}), 400
    product = Product(id=str(uuid.uuid4()), store_id=store.id, name=name, sku=sku, current_price=price)
    db.session.add(product); db.session.commit(); return jsonify({"data": product.to_dict()}), 201

@catalog_bp.get("/products/<product_id>")
def get_product(product_id):
    product = db.session.get(Product, product_id); return jsonify(product.to_dict()) if product else (jsonify({"error": "Produto não encontrado"}), 404)

@catalog_bp.get("/products/<product_id>/history")
def product_history(product_id):
    product = db.session.get(Product, product_id)
    if not product: return jsonify({"error": "Produto não encontrado"}), 404
    page = max(request.args.get("page", 1, type=int), 1); per_page = min(max(request.args.get("per_page", 20, type=int), 1), 100)
    pagination = PriceChange.query.filter_by(product_id=product_id).order_by(PriceChange.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({"product": product.to_dict(), "data": [item.to_dict() for item in pagination.items], "total": pagination.total, "pages": pagination.pages, "page": page, "per_page": per_page})

@catalog_bp.put("/products/<product_id>")
def update_product(product_id):
    product = db.session.get(Product, product_id)
    if not product: return jsonify({"error": "Produto não encontrado"}), 404
    data = _json()
    if "current_price" in data:
        try: price = float(data["current_price"])
        except (TypeError, ValueError): return jsonify({"error": "Preço inválido"}), 400
        if not math.isfinite(price): return jsonify({"error": "Preço deve ser um número finito"}), 400
        if price <= 0: return jsonify({"error": "Preço deve ser maior que zero"}), 400
        product.current_price = price
    limits = {"name": 160, "sku": 80}
    for field, maximum in limits.items():
        if field in data:
            value = str(data[field] or "").strip()
            if not value or len(value) > maximum:
                return jsonify({"error": f"{field} deve ter entre 1 e {maximum} caracteres"}), 400
            setattr(product, field, value)
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
            return jsonify({"error": "Já existe um produto com este SKU nesta loja"}), 409
        raise
    return jsonify({"data": product.to_dict()})

@catalog_bp.delete("/products/<product_id>")
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product: return jsonify({"error": "Produto não encontrado"}), 404
    if any(change.status in {"pending", "active"} for change in product.price_changes): return jsonify({"error": "Não é possível excluir produto com alterações abertas"}), 409
    try:
        for change in list(product.price_changes): db.session.delete(change)
        db.session.delete(product); db.session.commit()
    except Exception:
        db.session.rollback(); return jsonify({"error": "Não foi possível excluir o produto"}), 500
    return jsonify({"message": "Produto excluído com sucesso"})
