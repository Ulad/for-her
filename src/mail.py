from smtplib import SMTPException
from threading import Thread

from flask import Flask, current_app
from flask_mail import Message

from src import cfg, email
from src.log import get_logger

log = get_logger(__name__)


def send_async_email(app: Flask, msg: Message) -> None:
    with app.app_context():
        try:
            email.send(msg)
        except (SMTPException, AssertionError) as e:
            log.warning("Failed to send email, error: %s", e)
        else:
            log.info("Sent %r to %s", msg.subject, msg.recipients)


def send_email(
    *, subject: str, text_body: str, html_body: str | None = None, recipients: list[str | tuple[str, str]] | None = None
) -> None:
    if recipients is None and cfg.MAIL_USERNAME:
        recipients = [cfg.MAIL_USERNAME]

    msg = Message(subject, sender=cfg.MAIL_USERNAME, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()  # type: ignore[attr-defined]
