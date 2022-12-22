import os

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load = load_dotenv(os.path.join(BASE_DIR, '.env'))


class GlobalConfig:
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    DEBUG = False
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('APP_MAIL_PORT'))
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD', None)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG=False
    MAIL_DEFAULT_SENDER = os.environ.get('APP_MAIL_USERNAME', None)
    
    DOMAIN_FRONTEND = os.environ.get('DOMAIN_FRONTEND', None)
    
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', None)


class DevelopmentConfig(GlobalConfig):
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(GlobalConfig):
    
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db_test.sqlite3')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(GlobalConfig):
    pass


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)