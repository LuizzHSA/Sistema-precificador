import uuid
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from app import db
from app.models import PriceChange, Product, Store, ExecutionLog, AuditEvent
from app.services.automation import process_due_price_changes
from app.services.audit import record_audit

price_bp = Blueprint("price_changes", __name__, url_prefix="/api")


def _json():
    return request.get_json(silent=True) or {}


def _date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _price(value):
    try:
        result = float(value)
        return result if result > 0 else None
    except (TypeError, ValueError):
        return None


@price_bp.get("/price-changes")
@jwt_required()
def list_price_changes():
    query = PriceChange.query
    for field in ("status", "store_id", "product_id"):
        value = request.args.get(field)
        if value:
            query = query.filter(getattr(PriceChange, field) == value)
    search = request.args.get("search", "").strip()
    if search:
        query = query.join(Product).filter(or_(Product.name.ilike(f"%{search}%"), Product.sku.ilike(f"%{search}%"), PriceChange.reason.ilike(f"%{search}%")))
    if request.args.get("from"):
        start = _date(request.args["from"])
        if start:
            query = query.filter(PriceChange.effective_date >= start)
    if request.args.get("to"):
        end = _date(request.args["to"])
        if end:
            query = query.filter(PriceChange.effective_date <= end)
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)
    pagination = query.order_by(PriceChange.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({"data": [item.to_dict() for item in pagination.items], "items": [item.to_dict() for item in pagination.items], "total": pagination.total, "pages": pagination.pages, "page": page, "current_page": page, "per_page": per_page})


@price_bp.get("/price-changes/<price_change_id>")
@jwt_required()
def get_price_change(price_change_id):
    item = db.session.get(PriceChange, price_change_id)
    return jsonify(item.to_dict()) if item else (jsonify({"error": "Alteração de preço não encontrada"}), 404)


@price_bp.post("/price-changes")
@jwt_required()
def create_price_change():
    data = _json()
    required = [field for field in ("store_id", "product_id", "new_price", "effective_date") if data.get(field) in (None, "")]
    if required:
        return jsonify({"error": f"Campos obrigatórios faltando: {', '.join(required)}"}), 400
    product = db.session.get(Product, data["product_id"])
    store = db.session.get(Store, data["store_id"])
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    if not store:
        return jsonify({"error": "Loja não encontrada"}), 404
    if product.store_id != store.id:
        return jsonify({"error": "Produto não pertence à loja informada"}), 400
    new_price = _price(data["new_price"])
    effective_date = _date(data["effective_date"])
    if new_price is None:
        return jsonify({"error": "Novo preço deve ser maior que zero"}), 400
    if effective_date is None:
        return jsonify({"error": "Data efetiva inválida"}), 400
    item = PriceChange(id=str(uuid.uuid4()), store_id=store.id, product_id=product.id, current_price=float(product.current_price), new_price=new_price, effective_date=effective_date, reason=data.get("reason", ""), status="pending")
    db.session.add(item)
    record_audit("price_change.created", "price_change", item.id, {"new_price": new_price, "product_id": product.id})
    db.session.commit()
    return jsonify({"message": "Alteração de preço criada com sucesso", "data": item.to_dict()}), 201


@price_bp.put("/price-changes/<price_change_id>")
@jwt_required()
def update_price_change(price_change_id):
    item = db.session.get(PriceChange, price_change_id)
    if not item:
        return jsonify({"error": "Alteração de preço não encontrada"}), 404
    if item.status not in {"pending", "active"}:
        return jsonify({"error": f"Não é possível atualizar uma alteração com status {item.status}"}), 400
    data = _json()
    if "new_price" in data:
        price = _price(data["new_price"])
        if price is None:
            return jsonify({"error": "Novo preço deve ser maior que zero"}), 400
        item.new_price = price
    if "effective_date" in data:
        date = _date(data["effective_date"])
        if date is None:
            return jsonify({"error": "Data efetiva inválida"}), 400
        item.effective_date = date
    if "reason" in data:
        item.reason = data["reason"]
    record_audit("price_change.updated", "price_change", item.id, {"status": item.status})
    db.session.commit()
    return jsonify({"message": "Alteração de preço atualizada com sucesso", "data": item.to_dict()})


@price_bp.post("/price-changes/<price_change_id>/activate")
@jwt_required()
def activate_price_change(price_change_id):
    item = db.session.get(PriceChange, price_change_id)
    if not item:
        return jsonify({"error": "Alteração de preço não encontrada"}), 404
    if item.status != "pending":
        return jsonify({"error": "Apenas alterações pendentes podem ser ativadas"}), 400
    item.status = "active"
    record_audit("price_change.activated", "price_change", item.id)
    db.session.commit()
    return jsonify({"message": "Alteração ativada com sucesso", "data": item.to_dict()})


@price_bp.post("/price-changes/<price_change_id>/execute")
@jwt_required()
def execute_price_change(price_change_id):
    item = db.session.get(PriceChange, price_change_id)
    if not item:
        return jsonify({"error": "Alteração de preço não encontrada"}), 404
    if item.status != "active":
        return jsonify({"error": "Apenas alterações ativas podem ser executadas"}), 400
    item.product.current_price = item.new_price
    item.status = "executed"
    item.executed_at = datetime.utcnow()
    record_audit("price_change.executed", "price_change", item.id, {"new_price": item.new_price})
    db.session.commit()
    return jsonify({"message": "Alteração de preço executada com sucesso", "data": item.to_dict()})


@price_bp.delete("/price-changes/<price_change_id>")
@jwt_required()
def cancel_price_change(price_change_id):
    item = db.session.get(PriceChange, price_change_id)
    if not item:
        return jsonify({"error": "Alteração de preço não encontrada"}), 404
    if item.status in {"executed", "cancelled"}:
        return jsonify({"error": "A alteração não pode ser cancelada neste status"}), 400
    item.status = "cancelled"
    record_audit("price_change.cancelled", "price_change", item.id)
    db.session.commit()
    return jsonify({"message": "Alteração de preço cancelada com sucesso", "data": item.to_dict()})


@price_bp.post("/automation/run")
@jwt_required()
def run_automation():
    result = process_due_price_changes()
    return jsonify(result), 200


@price_bp.get("/execution-logs")
@jwt_required()
def execution_logs():
    logs = ExecutionLog.query.order_by(ExecutionLog.created_at.desc()).limit(100).all()
    return jsonify([{"id": log.id, "price_change_id": log.price_change_id, "status": log.status,
                    "message": log.message, "created_at": log.created_at.isoformat()} for log in logs])


@price_bp.get("/audit-events")
@jwt_required()
def audit_events():
    events = AuditEvent.query.order_by(AuditEvent.created_at.desc()).limit(100).all()
    return jsonify([{"id": event.id, "action": event.action, "entity_type": event.entity_type,
                    "entity_id": event.entity_id, "payload": event.payload,
                    "created_at": event.created_at.isoformat()} for event in events])


@price_bp.get("/dashboard")
@jwt_required()
def dashboard():
    counts = {status: PriceChange.query.filter_by(status=status).count() for status in PriceChange.VALID_STATUSES}
    recent = PriceChange.query.order_by(PriceChange.created_at.desc()).limit(5).all()
    today = datetime.utcnow().date()
    today_items = [item for item in PriceChange.query.all() if item.created_at and item.created_at.date() == today]
    all_items = PriceChange.query.all()
    increases = sorted((item for item in all_items if item.price_difference > 0), key=lambda item: item.price_difference, reverse=True)[:5]
    reductions = sorted((item for item in all_items if item.price_difference < 0), key=lambda item: item.price_difference)[:5]
    return jsonify({"products": Product.query.count(), "stores": Store.query.count(), "price_changes": sum(counts.values()),
                    "pending": counts["pending"], "active": counts["active"], "executed": counts["executed"], "cancelled": counts["cancelled"],
                    "today": len(today_items), "today_changes": len(today_items), "recent": [item.to_dict() for item in recent],
                    "largest_increases": [item.to_dict() for item in increases], "largest_reductions": [item.to_dict() for item in reductions]})
