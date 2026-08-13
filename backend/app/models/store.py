from datetime import datetime
from app import db


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    products = db.relationship("Product", back_populates="store", cascade="all, delete-orphan")
    price_changes = db.relationship("PriceChange", back_populates="store")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "phone": self.phone,
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None}


class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = (db.UniqueConstraint("store_id", "sku", name="uq_product_store_sku"),)

    id = db.Column(db.String(36), primary_key=True)
    store_id = db.Column(db.String(36), db.ForeignKey("stores.id"), nullable=False, index=True)
    name = db.Column(db.String(160), nullable=False)
    sku = db.Column(db.String(80), nullable=False, index=True)
    current_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    store = db.relationship("Store", back_populates="products")
    price_changes = db.relationship("PriceChange", back_populates="product")

    def to_dict(self):
        return {"id": self.id, "store_id": self.store_id, "store": self.store.name if self.store else None,
                "name": self.name, "sku": self.sku, "current_price": self.current_price,
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None}


class PriceChange(db.Model):
    __tablename__ = "price_changes"
    VALID_STATUSES = {"pending", "active", "executed", "cancelled"}

    id = db.Column(db.String(36), primary_key=True)
    store_id = db.Column(db.String(36), db.ForeignKey("stores.id"), nullable=False, index=True)
    product_id = db.Column(db.String(36), db.ForeignKey("products.id"), nullable=False, index=True)
    current_price = db.Column(db.Float, nullable=False)
    new_price = db.Column(db.Float, nullable=False)
    effective_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    reason = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    executed_at = db.Column(db.DateTime, nullable=True)
    store = db.relationship("Store", back_populates="price_changes")
    product = db.relationship("Product", back_populates="price_changes")

    @property
    def price_difference(self):
        return round(self.new_price - self.current_price, 2)

    @property
    def percentage_change(self):
        if not self.current_price:
            return 0
        return round((self.price_difference / self.current_price) * 100, 2)

    def to_dict(self):
        return {"id": self.id, "store_id": self.store_id, "store": self.store.name if self.store else None,
                "product_id": self.product_id, "product": self.product.name if self.product else None,
                "sku": self.product.sku if self.product else None, "current_price": self.current_price,
                "new_price": self.new_price, "price_difference": self.price_difference,
                "percentage_change": self.percentage_change, "effective_date": self.effective_date.isoformat() if self.effective_date else None,
                "status": self.status, "reason": self.reason, "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "executed_at": self.executed_at.isoformat() if self.executed_at else None}
