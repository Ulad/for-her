import atexit
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from smtplib import SMTPException

from flask import Flask, current_app
from flask_mail import Message

from src.extensions import email

log = getLogger(__name__)

_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="email")
atexit.register(_executor.shutdown, wait=True)


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
    if recipients is None and current_app.config["MAIL_USERNAME"]:
        recipients = [current_app.config["MAIL_USERNAME"]]

    msg = Message(subject, sender=current_app.config["MAIL_USERNAME"], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    _executor.submit(send_async_email, current_app._get_current_object(), msg)  # type: ignore[attr-defined]
