from flask import Flask

from src.config import Config, get_cfg
from src.extensions import email
from src.handlers.errors import register_error
from src.handlers.misc import register_misc
from src.log import register_mail_logging, setup_logging


def create_app(config_class: Config | None = None) -> Flask:
    config_class = config_class or get_cfg()
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_logging()

    email.init_app(app)

    if not app.debug:
        register_mail_logging(app)

    register_misc(app)
    register_error(app)

    return app
