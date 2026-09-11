from logging import getLogger

from flask import Flask, Response, request

log = getLogger(__name__)


def register_misc(app: Flask) -> None:
    @app.before_request
    def log_request_info() -> None:
        if request.method == "POST":
            if request.is_json:
                log.info("JSON body: %s", request.get_json())
            else:
                log.info("Form data: %s", dict(request.form))

    @app.route("/favicon.ico")
    def favicon() -> Response:
        return app.send_static_file("img/favicon.ico")
