import logging
from flask import has_app_context
from app import db
from app.models.automation import AuditEvent

logger = logging.getLogger(__name__)


def record_audit(action, entity_type, entity_id, payload=None):
    if not has_app_context():
        logger.warning("audit_without_app_context", extra={"action": action, "entity_id": entity_id})
        return None
    event = AuditEvent(action=action, entity_type=entity_type, entity_id=str(entity_id), payload=payload or {})
    db.session.add(event)
    return event
