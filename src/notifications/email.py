"""https://red-mail.readthedocs.io/en/stable/tutorials/config.html#gmail."""

from collections.abc import Iterable

from redmail.email import gmail

from src.config import get_cfg
from src.log import get_logger

log = get_logger(__name__)


def _configure() -> bool:
    if gmail.username and gmail.password:
        return True

    try:
        cfg = get_cfg()
        username, password = cfg.GMAIL_USERNAME, cfg.GMAIL_PASSWORD
    except AttributeError:
        username = password = None

    if not (username and password):
        log.warning("Couldn't configure notifications.")
        return False

    gmail.username = username
    gmail.password = password.get_secret_value()
    return True


def send_notification(*, subject: str, text: str, receivers: Iterable[str] | None = None) -> None:
    """If `receivers` is None, sends to the configured Gmail account itself."""
    if not _configure():
        return

    targets = list(receivers) if receivers else [gmail.username]
    try:
        gmail.send(subject=subject, text=text, receivers=targets)
        log.info("Sent %r to %s", subject, targets)
    except Exception:
        log.exception("Failed to send %r to %s", subject, targets)


def notify_choice(text: str) -> None:
    send_notification(subject="Date picked", text=text)


if __name__ == "__main__":
    notify_choice("test notification")
