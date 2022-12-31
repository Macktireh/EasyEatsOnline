# import werkzeug 
# werkzeug.cached_property = werkzeug.utils.cached_property
import collections
collections.MutableMapping = collections.abc.MutableMapping
from typing import Tuple

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin

from config.settings import DevelopmentConfig, ProductionConfig, TestingConfig
from admin import HomeAdminModelView


db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_name: str) -> Tuple[Flask, Admin]:
    print("************************************************************************")
    print()
    print(config_name)
    print()
    print("************************************************************************")
    app = Flask(__name__)
    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        raise Exception('Unknown configuration')
    db.init_app(app)
    JWTManager(app)
    LoginManager(app)
    admin = Admin(app, index_view=HomeAdminModelView(name='Overview'), name="Control Panel")
    flask_bcrypt.init_app(app)

    return app, admin