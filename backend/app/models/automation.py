from datetime import datetime
from app import db


class ExecutionLog(db.Model):
    __tablename__ = "execution_logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price_change_id = db.Column(db.String(36), db.ForeignKey("price_changes.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    price_change = db.relationship("PriceChange", back_populates="execution_logs")


class AuditEvent(db.Model):
    __tablename__ = "audit_events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(120), nullable=False, index=True)
    entity_type = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.String(120), nullable=False, index=True)
    payload = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
