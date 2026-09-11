from logging import getLogger
from typing import TYPE_CHECKING

from flask import Flask, render_template

log = getLogger(__name__)

if TYPE_CHECKING:
    from werkzeug.exceptions import HTTPException


def register_error(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(_error: "HTTPException") -> tuple[str, int]:
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error: Exception) -> tuple[str, int]:
        log.error("Unhandled server error")
        return render_template("errors/500.html"), 500
