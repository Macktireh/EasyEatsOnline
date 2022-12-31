import os
import secrets

from datetime import timedelta
from pathlib import Path
# from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
# load = load_dotenv(os.path.join(BASE_DIR, '.env'))


class GlobalConfig:
    
    DEBUG: bool = False
    SECRET_KEY: str = os.environ.get('SECRET_KEY', secrets.token_urlsafe(128))
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', secrets.token_urlsafe(128))
    JWT_ACCESS_TOKEN_EXPIRES: str = timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES: str = timedelta(days=1)
    SECURITY_PASSWORD_SALT: str = os.environ.get('SECURITY_PASSWORD_SALT', secrets.token_urlsafe(128))
    MAIL_SERVER: str = 'smtp.gmail.com'
    MAIL_PORT: int = 587
    MAIL_USERNAME: str = os.environ.get('APP_MAIL_USERNAME')
    MAIL_PASSWORD: str = os.environ.get('APP_MAIL_PASSWORD')
    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False
    MAIL_DEBUG=False
    MAIL_DEFAULT_SENDER: str = os.environ.get('APP_MAIL_USERNAME')
    DOMAIN_FRONTEND: str = os.environ.get('DOMAIN_FRONTEND')


class DevelopmentConfig(GlobalConfig):
    
    DEBUG: bool = True
    TYPE_DATABASE = os.environ.get('TYPE_DATABASE', 'sqlite')
    SQLALCHEMY_DATABASE_URI_SQLITE: str = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI_POSTGRESQL: str = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
    SQLALCHEMY_DATABASE_URI: str = SQLALCHEMY_DATABASE_URI_POSTGRESQL if TYPE_DATABASE == 'postgresql' else SQLALCHEMY_DATABASE_URI_SQLITE
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class TestingConfig(GlobalConfig):
    
    DEBUG: bool = True
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///' + os.path.join(BASE_DIR, 'db_test.sqlite3')
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class ProductionConfig(GlobalConfig):
    pass