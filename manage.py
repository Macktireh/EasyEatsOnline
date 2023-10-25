import click

from typing import Any, Dict, Literal, Tuple, Union
from werkzeug.exceptions import NotFound, Forbidden, BadRequest

from flask import render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.cli import with_appcontext
from admin.register import registerAdmin

from app import createApp, db
from config.settings import getEnvVar
from repository.userRepository import userRepository
from utils import status
from utils.cli import createSuperUserCli, testCli

# models
from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order
from models.cart import Cart

# routes
from controllers import apiRoute
from controllers.adminAuthController import adminLogin


# create app flask
flask_app, admin = createApp(getEnvVar("FLASK_ENV", "development"))

migrate = Migrate(flask_app, db)
registerAdmin(admin, db)

# register api routes
flask_app.register_blueprint(apiRoute)
flask_app.register_blueprint(adminLogin)

# flask login configuration
login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = "admin.login"


@flask_app.route("/")
def home() -> Any:
    return render_template("home/home.html")


@login_manager.user_loader
def user_loader(id: Union[str, int]) -> User:
    return userRepository.getById(int(id))


@login_manager.request_loader
def request_loader(request) -> None:
    return


@flask_app.errorhandler(status.HTTP_403_FORBIDDEN)
def forbidden(e: Forbidden) -> Tuple[Dict[str, str], Literal[403]]:
    return {
        "message": "Forbidden",
        "error": str(e),
    }, status.HTTP_403_FORBIDDEN


@flask_app.errorhandler(status.HTTP_404_NOT_FOUND)
def notfound(e: NotFound) -> Tuple[Dict[str, str], Literal[404]]:
    print()
    print("manage.py: notfound", e)
    print()
    return {
        "message": "Endpoint Not Found",
        "error": str(e),
    }, status.HTTP_404_NOT_FOUND


@flask_app.errorhandler(status.HTTP_400_BAD_REQUEST)
def badrequest(e: BadRequest) -> Tuple[Dict[str, str], Literal[404]]:
    return {
        "messagess": "Bad Request",
        "error": str(e),
    }, status.HTTP_400_BAD_REQUEST


@click.command(name="createsuperuser")
@with_appcontext
def createsuperuser() -> None:
    """Create a super user"""
    createSuperUserCli()


@click.command(name="test")
@with_appcontext
def test() -> None:
    """Runs the unit tests."""
    testCli()


flask_app.cli.add_command(createsuperuser)
flask_app.cli.add_command(test)
