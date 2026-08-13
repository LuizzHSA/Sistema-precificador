import logging
from datetime import datetime
from app import db
from app.models import PriceChange, ExecutionLog
from app.services.notifications import send_price_change_notification
from app.services.audit import record_audit

logger = logging.getLogger(__name__)


def process_due_price_changes(max_retries=3):
    """Executa alterações ativas cuja data efetiva já chegou.

    Cada item possui uma transação própria para que uma falha não bloqueie os demais.
    """
    now = datetime.utcnow()
    due = PriceChange.query.filter(
        PriceChange.status == "active", PriceChange.effective_date <= now
    ).all()
    results = {"processed": 0, "failed": 0, "skipped": 0, "items": []}
    for item in due:
        try:
            if item.retry_count >= max_retries:
                results["skipped"] += 1
                continue
            item.product.current_price = item.new_price
            item.status = "executed"
            item.executed_at = datetime.utcnow()
            item.retry_count = 0
            log = ExecutionLog(price_change_id=item.id, status="success", message="Alteração executada automaticamente")
            db.session.add(log)
            record_audit("price_change.auto_execute", "price_change", item.id, {"new_price": item.new_price})
            db.session.commit()
            try:
                send_price_change_notification(item, "executed")
            except Exception:  # noqa: BLE001
                logger.exception("price_change_notification_failed", extra={"price_change_id": item.id})
            results["processed"] += 1
            results["items"].append(item.id)
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
            item.retry_count = (item.retry_count or 0) + 1
            db.session.add(ExecutionLog(price_change_id=item.id, status="failed", message=str(exc)))
            db.session.commit()
            logger.exception("price_change_execution_failed", extra={"price_change_id": item.id})
            results["failed"] += 1
            results["items"].append(item.id)
    return results
