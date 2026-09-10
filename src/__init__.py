from flask import Flask
from flask_mail import Mail

from src.config import Config, get_cfg
from src.handlers.errors import register_error
from src.handlers.misc import register_misc

email = Mail()
cfg = get_cfg()


def create_app(config_class: Config = cfg) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    email.init_app(app)
    register_misc(app)
    register_error(app)

    return app
