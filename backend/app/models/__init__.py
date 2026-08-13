from datetime import datetime
from app import db

class Store(db.Model):
    """Modelo da Loja"""
    __tablename__ = 'stores'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    price_changes = db.relationship('PriceChange', back_populates='store', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class Product(db.Model):
    """Modelo do Produto"""
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True)
    store_id = db.Column(db.String(36), db.ForeignKey('stores.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(255), nullable=False)
    current_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    price_changes = db.relationship('PriceChange', back_populates='product', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'name': self.name,
            'sku': self.sku,
            'current_price': float(self.current_price),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class PriceChange(db.Model):
    """Modelo de Alteração de Preço"""
    __tablename__ = 'price_changes'
    
    id = db.Column(db.String(36), primary_key=True)
    store_id = db.Column(db.String(36), db.ForeignKey('stores.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    current_price = db.Column(db.Numeric(10, 2), nullable=False)
    new_price = db.Column(db.Numeric(10, 2), nullable=False)
    effective_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, active, executed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    executed_at = db.Column(db.DateTime, nullable=True)
    reason = db.Column(db.Text)
    
    # Relacionamentos
    store = db.relationship('Store', back_populates='price_changes')
    product = db.relationship('Product', back_populates='price_changes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'current_price': float(self.current_price),
            'new_price': float(self.new_price),
            'effective_date': self.effective_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'reason': self.reason,
        }
    
    def price_difference(self):
        """Calcular diferença de preço"""
        return float(self.new_price) - float(self.current_price)
    
    def percentage_change(self):
        """Calcular percentual de mudança"""
        if self.current_price == 0:
            return 0
        return (self.price_difference() / float(self.current_price)) * 100
