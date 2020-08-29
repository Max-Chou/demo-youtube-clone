from flask import Flask
from .extensions import db, login_manager
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .page import page
    app.register_blueprint(page)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
