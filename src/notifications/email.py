"""https://red-mail.readthedocs.io/en/stable/tutorials/config.html#gmail."""

from redmail.email import gmail

from src.config import get_cfg
from src.log import get_logger

log = get_logger(__name__)

gmail.username = get_cfg().GMAIL_USERNAME
gmail.password = get_cfg().GMAIL_PASSWORD.get_secret_value()


def notify_choice(text: str) -> None:
    receivers = gmail.username
    log.info("Sending email to: %s", receivers)

    try:
        gmail.send(subject="Date picked", receivers=receivers, text=text)
    except Exception:
        log.exception("Can't sent email to %s", receivers)


if __name__ == "__main__":
    notify_choice("test notification")
