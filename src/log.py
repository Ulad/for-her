from __future__ import annotations

import logging
import sys
from logging.config import dictConfig
from typing import TYPE_CHECKING, ClassVar, override

from flask import has_request_context, request

from src.mail import send_email

if TYPE_CHECKING:
    from logging import LogRecord
    from types import TracebackType

    from flask import Flask


APP_LOGGER_NAME = "src"
app_log = logging.getLogger(APP_LOGGER_NAME)
LOG_FORMAT = "%(asctime)s - [%(levelname)-8s] - %(module)s - %(funcName)s - %(lineno)s - %(message)s"


def handle_uncaught_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    app_log.critical(
        "Uncaught exception, application will terminate.",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


class ColoredFormatter(logging.Formatter):
    """Colored output formatter."""

    COLORS: ClassVar = {
        "DEBUG": "\033[0;37m",  # Light gray
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\x1b[31;1m",  # Bold red
        "RESET": "\033[0m",  # Reset color
    }

    @override
    def format(self, record: LogRecord) -> str:
        """Format a `LogRecord` into a colored string."""
        msg = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f"{color}{msg}{self.COLORS['RESET']}"


def setup_logging(*, level: str | int = "INFO") -> None:
    """Set up logging."""
    sys.excepthook = handle_uncaught_exception

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "coloredFormatter": {
                    "()": ColoredFormatter,
                    "format": LOG_FORMAT,
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
            },
            "handlers": {
                "consoleHandler": {
                    "class": "logging.StreamHandler",
                    "level": level,
                    "formatter": "coloredFormatter",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                APP_LOGGER_NAME: {
                    "level": level,
                    "handlers": ["consoleHandler"],
                    "propagate": False,
                },
                "werkzeug": {
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )


class MailHandler(logging.Handler):
    """Logging handler that emails error records using the app's async mail module."""

    def __init__(self, app: Flask, *, recipients: list[str | tuple[str, str]] | None) -> None:
        super().__init__()
        self.app = app
        self.recipients = recipients

    @override
    def emit(self, record: LogRecord) -> None:
        try:
            body = self.format(record)
            if has_request_context():
                body += (
                    f"\n\nRequest Info:"
                    f"\nURL:        {request.url}"
                    f"\nMethod:     {request.method}"
                    f"\nIP:         {request.remote_addr}"
                    f"\nUser-Agent: {request.headers.get('User-Agent')}"
                )
            send_email(
                subject=f"[{record.levelname}] {record.getMessage()[:80]}",
                text_body=body,
                recipients=self.recipients,
            )
        except Exception:  # noqa: BLE001
            self.handleError(record)


def register_mail_logging(
    app: Flask, *, recipients: list[str | tuple[str, str]] | None = None, level: int = logging.ERROR
) -> None:
    """Attach a mail handler to the app logger."""
    handler = MailHandler(app, recipients=recipients)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z"))
    logging.getLogger(APP_LOGGER_NAME).addHandler(handler)
