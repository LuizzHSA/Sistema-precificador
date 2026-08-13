from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import uuid
from app import db
from app.models import PriceChange, Product, Store

price_bp = Blueprint('prices', __name__, url_prefix='/api/price-changes')

@price_bp.route('', methods=['GET'])
@jwt_required()
def get_price_changes():
    """Listar alterações de preço com filtros"""
    store_id = request.args.get('store_id')
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = PriceChange.query
    
    if store_id:
        query = query.filter_by(store_id=store_id)
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(PriceChange.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [pc.to_dict() for pc in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
    }), 200

@price_bp.route('/<price_change_id>', methods=['GET'])
@jwt_required()
def get_price_change(price_change_id):
    """Obter detalhes de uma alteração de preço"""
    price_change = PriceChange.query.get(price_change_id)
    
    if not price_change:
        return jsonify({'error': 'Alteração de preço não encontrada'}), 404
    
    return jsonify(price_change.to_dict()), 200

@price_bp.route('', methods=['POST'])
@jwt_required()
def create_price_change():
    """Criar nova alteração de preço"""
    data = request.get_json()
    
    # Validações
    required_fields = ['store_id', 'product_id', 'new_price', 'effective_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400
    
    # Verificar se produto existe
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    # Criar nova alteração
    price_change = PriceChange(
        id=str(uuid.uuid4()),
        store_id=data['store_id'],
        product_id=data['product_id'],
        current_price=product.current_price,
        new_price=float(data['new_price']),
        effective_date=datetime.fromisoformat(data['effective_date']),
        status='pending',
        reason=data.get('reason', '')
    )
    
    db.session.add(price_change)
    db.session.commit()
    
    return jsonify({
        'message': 'Alteração de preço criada com sucesso',
        'data': price_change.to_dict()
    }), 201

@price_bp.route('/<price_change_id>', methods=['PUT'])
@jwt_required()
def update_price_change(price_change_id):
    """Atualizar alteração de preço"""
    price_change = PriceChange.query.get(price_change_id)
    
    if not price_change:
        return jsonify({'error': 'Alteração de preço não encontrada'}), 404
    
    if price_change.status not in ['pending', 'active']:
        return jsonify({'error': f'Não é possível atualizar uma alteração com status {price_change.status}'}), 400
    
    data = request.get_json()
    
    if 'new_price' in data:
        price_change.new_price = float(data['new_price'])
    if 'effective_date' in data:
        price_change.effective_date = datetime.fromisoformat(data['effective_date'])
    if 'reason' in data:
        price_change.reason = data['reason']
    
    price_change.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Alteração de preço atualizada com sucesso',
        'data': price_change.to_dict()
    }), 200

@price_bp.route('/<price_change_id>/execute', methods=['POST'])
@jwt_required()
def execute_price_change(price_change_id):
    """Executar alteração de preço"""
    price_change = PriceChange.query.get(price_change_id)
    
    if not price_change:
        return jsonify({'error': 'Alteração de preço não encontrada'}), 404
    
    if price_change.status != 'active':
        return jsonify({'error': f'Apenas alterações ativas podem ser executadas'}), 400
    
    # Atualizar preço do produto
    price_change.product.current_price = price_change.new_price
    price_change.status = 'executed'
    price_change.executed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Alteração de preço executada com sucesso',
        'data': price_change.to_dict()
    }), 200

@price_bp.route('/<price_change_id>', methods=['DELETE'])
@jwt_required()
def cancel_price_change(price_change_id):
    """Cancelar alteração de preço"""
    price_change = PriceChange.query.get(price_change_id)
    
    if not price_change:
        return jsonify({'error': 'Alteração de preço não encontrada'}), 404
    
    if price_change.status == 'executed':
        return jsonify({'error': 'Não é possível cancelar uma alteração já executada'}), 400
    
    price_change.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Alteração de preço cancelada com sucesso'}), 200
