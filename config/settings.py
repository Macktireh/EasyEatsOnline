import os
import secrets
from datetime import timedelta
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load = load_dotenv(os.path.join(BASE_DIR, ".env"))

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")


def getEnvVar(varName: str, default: str | None = None, required: bool = True) -> str | None:
    value = os.environ.get(varName, default)
    if required and not value:
        raise Exception(f"Environment variable {varName} is required")
    return value


class GlobalConfig:
    DEBUG = False
    FLASK_DEBUG = False
    FLASK_ENV = getEnvVar("FLASK_ENV", "development")
    SECRET_KEY = getEnvVar("SECRET_KEY", secrets.token_hex(32))
    JWT_SECRET_KEY = getEnvVar("JWT_SECRET_KEY", secrets.token_hex(32))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SECURITY_PASSWORD_SALT = getEnvVar("SECURITY_PASSWORD_SALT", secrets.token_hex(32))
    SQLALCHEMY_ECHO = False
    CLIENT_BASE_URL = getEnvVar("CLIENT_BASE_URL", "http://localhost:3000")
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_FOLDER = "translations"
    LANGUAGES = {
        "en": "English",
        "fr": "French",
    }
    BABEL_DEFAULT_TIMEZONE = "Europe/Paris"

    MAIL_SERVER = getEnvVar("APP_MAIL_SERVER", required=False)
    MAIL_PORT = getEnvVar("APP_MAIL_PORT", required=False)
    MAIL_USERNAME = getEnvVar("APP_MAIL_USERNAME", required=False)
    MAIL_PASSWORD = getEnvVar("APP_MAIL_PASSWORD", required=False)
    MAIL_DEFAULT_SENDER = getEnvVar("APP_MAIL_USERNAME", required=False)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    TYPE_DATABASE = getEnvVar("TYPE_DATABASE", "sqlite")
    SQLALCHEMY_DATABASE_URI_SQLITE = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
    if TYPE_DATABASE == "postgresql":
        SQLALCHEMY_DATABASE_URI = f"postgresql://{getEnvVar('POSTGRES_USER')}:{getEnvVar('POSTGRES_PASSWORD')}@{getEnvVar('POSTGRES_HOST')}:{getEnvVar('POSTGRES_PORT')}/{getEnvVar('POSTGRES_DB')}"  # noqa
    else:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_SQLITE
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True


class DevelopmentConfig(GlobalConfig):
    DEVELOPMENT = True
    DEBUG = True
    MAIL_DEBUG = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREFERRED_URL_SCHEME = "http"


class TestingConfig(GlobalConfig):
    DEBUG = True
    TESTING = True
    MAIL_DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "db_test.sqlite3")
    PREFERRED_URL_SCHEME = "http"


class ProductionConfig(GlobalConfig):
    PRODUCTION = True
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{getEnvVar('POSTGRES_USER')}:{getEnvVar('POSTGRES_PASSWORD')}@{getEnvVar('POSTGRES_HOST')}:{getEnvVar('POSTGRES_PORT')}/{getEnvVar('POSTGRES_DB')}"  # noqa


class PostmanConfig(DevelopmentConfig):
    SERVER_NAME = getEnvVar("SERVER_NAME", "localhost:5000")
    APPLICATION_ROOT = getEnvVar("APPLICATION_ROOT", "/")
    PREFERRED_URL_SCHEME = "http"


class ConfigName(Enum):
    DEVELOPEMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    POSTMAN = "postman"


configByName = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig, postman=PostmanConfig
)
