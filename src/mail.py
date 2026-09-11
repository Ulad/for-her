from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from smtplib import SMTPException

from flask import Flask, current_app
from flask_mail import Message

from src.extensions import cfg, email

log = getLogger(__name__)

_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="email")


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
    _executor.submit(send_async_email, current_app._get_current_object(), msg)  # type: ignore[attr-defined]
