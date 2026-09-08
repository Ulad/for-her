from __future__ import annotations

import logging
import sys
from logging.config import dictConfig
from typing import TYPE_CHECKING, ClassVar, override

if TYPE_CHECKING:
    from logging import Logger, LogRecord
    from types import TracebackType

APP_LOGGER_NAME = "src"
app_log = logging.getLogger(APP_LOGGER_NAME)
LOG_FORMAT = "%(asctime)s - [%(levelname)-8s] - %(module)s - %(funcName)s - %(lineno)s - %(message)s"


def handle_uncaught_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> None:
    app_log.critical(
        "Uncaught exception, application will terminate.",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


sys.excepthook = handle_uncaught_exception


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


def get_logger(name: str | None = None) -> Logger:
    """
    Get a logger with the given name, ensuring logging is configured.

    Call this in modules that need logging instead of configuring logging again.
    """
    setup_logging()
    if name is None:
        return logging.getLogger(APP_LOGGER_NAME)
    if name == "__main__":
        return logging.getLogger(f"{APP_LOGGER_NAME}.__main__")
    return logging.getLogger(name)
