import os

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load = load_dotenv(os.path.join(BASE_DIR, ".env"))


def getEnvVar(varName: str, default: str | None = None, required: bool = True) -> str | None:
    value = os.environ.get(varName, default)
    if required and not value:
        raise Exception(f"Environment variable {varName} is required")
    return value


class GlobalConfig:
    DEBUG = False
    FLASK_DEBUG = False
    FLASK_ENV = getEnvVar("FLASK_ENV", "development")
    SECRET_KEY = getEnvVar("SECRET_KEY", "f0ji6t2hiltv5mUcgFOJIm1baDsGx3ye6Gj0NGo_Xuw")
    JWT_SECRET_KEY = getEnvVar("JWT_SECRET_KEY", "OaWUwNfHpgoVk_0ykn-EV54El1M4FBEd0HpbjcVGCOI")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    SECURITY_PASSWORD_SALT = getEnvVar("SECURITY_PASSWORD_SALT", "O6yfbOoAzei3kt5x4i9q9YELoAtPw3ZbKeZpUStbkso")
    SQLALCHEMY_ECHO = False

    MAIL_SERVER = getEnvVar("APP_MAIL_SERVER", required=False)
    MAIL_PORT = getEnvVar("APP_MAIL_PORT", required=False)
    MAIL_USERNAME = getEnvVar("APP_MAIL_USERNAME", required=False)
    MAIL_PASSWORD = getEnvVar("APP_MAIL_PASSWORD", required=False)
    MAIL_DEFAULT_SENDER = getEnvVar("APP_MAIL_USERNAME", required=False)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    DOMAIN_FRONTEND = getEnvVar("DOMAIN_FRONTEND", "localhost:3000")

    TYPE_DATABASE = getEnvVar("TYPE_DATABASE", "sqlite")
    SQLALCHEMY_DATABASE_URI_SQLITE = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
    if TYPE_DATABASE == "postgresql":
        SQLALCHEMY_DATABASE_URI = f"postgresql://{getEnvVar('POSTGRES_USER')}:{getEnvVar('POSTGRES_PASSWORD')}@{getEnvVar('POSTGRES_HOST')}:{getEnvVar('POSTGRES_PORT')}/{getEnvVar('POSTGRES_DB')}"  # noqa
    else:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_SQLITE


class DevelopmentConfig(GlobalConfig):
    DEBUG = True
    FLASK_DEBUG = True
    MAIL_DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(GlobalConfig):
    DEBUG = True
    TESTING = True
    MAIL_DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "db_test.sqlite3")


class ProductionConfig(GlobalConfig):
    pass


config_by_name = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
