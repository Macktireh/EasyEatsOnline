from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config.settings import ConfigName, configByName

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def createApp(configName: ConfigName) -> Flask:
    app = Flask(__name__)
    try:
        app.config.from_object(configByName[configName])
    except KeyError as e:
        raise Exception("Unknown configuration") from e
    db.init_app(app)
    JWTManager(app)
    flask_bcrypt.init_app(app)

    return app
