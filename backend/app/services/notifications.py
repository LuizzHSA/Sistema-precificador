import logging
import smtplib
from email.message import EmailMessage
from flask import current_app

logger = logging.getLogger(__name__)


def render_price_change_email(price_change, event):
    subject = f"Alteração de preço {event}: {price_change.product.name}"
    body = (
        f"Produto: {price_change.product.name}\n"
        f"Loja: {price_change.store.name}\n"
        f"Status: {event}\n"
        f"Preço anterior: R$ {price_change.current_price:.2f}\n"
        f"Novo preço: R$ {price_change.new_price:.2f}\n"
        f"Diferença: R$ {price_change.price_difference:.2f} ({price_change.percentage_change:.2f}%)\n"
    )
    return subject, body


def send_price_change_notification(price_change, event):
    recipient = current_app.config.get("NOTIFICATION_EMAIL")
    if not recipient:
        logger.info("notification_skipped", extra={"price_change_id": price_change.id, "event": event})
        return {"sent": False, "reason": "NOTIFICATION_EMAIL não configurado"}
    subject, body = render_price_change_email(price_change, event)
    host = current_app.config.get("SMTP_HOST")
    if not host:
        logger.info("notification_dry_run", extra={"to": recipient, "subject": subject, "body": body})
        return {"sent": False, "reason": "SMTP_HOST não configurado"}
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = current_app.config.get("SMTP_FROM", "noreply@localhost")
    message["To"] = recipient
    message.set_content(body)
    with smtplib.SMTP(host, current_app.config.get("SMTP_PORT", 587), timeout=10) as server:
        if current_app.config.get("SMTP_TLS", True):
            server.starttls()
        username = current_app.config.get("SMTP_USERNAME")
        password = current_app.config.get("SMTP_PASSWORD")
        if username and password:
            server.login(username, password)
        server.send_message(message)
    return {"sent": True, "to": recipient}
