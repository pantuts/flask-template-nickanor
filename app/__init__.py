from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from app.utils.assets import bundles
from config import config as Config

import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()


def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)

    # Register Jinja template functions
    from app.utils import register_template_utils
    register_template_utils(app)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    assets_env.register('app_css', bundles['app_css'])
    assets_env.register('app_js', bundles['app_js'])

    # Blueprints
    from app.views import main
    app.register_blueprint(main)

    return app
