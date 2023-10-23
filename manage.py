import click
import warnings

from typing import Any, Dict, Literal, Tuple, Union
from werkzeug.exceptions import NotFound, Forbidden, BadRequest

from flask import render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.cli import with_appcontext
from flask_admin.menu import MenuLink

from app import create_app, db
from config.settings import getEnvVar
from repository.userRepository import userRepository
from utils import status
from utils.cli import createsuperuserCli, testCli

# models
from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order
from models.cart import Cart

# Admin
from admin.user import UserAdmin
from admin.product import ProductAdmin
from admin.category import CategoryAdmin
from admin.cart import CartAdmin
from admin.order import OrderAdmin

# routes
from admin.auth.login import admin_login
from controllers import blueprint as blueprint_api

# create app flask
flask_app, admin = create_app(getEnvVar("FLASK_ENV", "development"))
migrate = Migrate(flask_app, db)

# save models in the admin panel
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", "Fields missing from ruleset", UserWarning)
    admin.add_view(UserAdmin(User, db.session))
admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(CategoryAdmin(Category, db.session))
admin.add_view(CartAdmin(Cart, db.session))
admin.add_view(OrderAdmin(Order, db.session))

# add menu items in the admin panel
admin.add_link(MenuLink(name="API Docs", category="", url="/api"))
admin.add_link(MenuLink(name="Logout", category="", url="/admin/auth/logout"))

# register api routes
flask_app.register_blueprint(blueprint_api)
flask_app.register_blueprint(admin_login)

# flask login configuration
login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = "admin.login"


@login_manager.user_loader
def user_loader(id: Union[str, int]) -> User:
    return userRepository.getById(int(id))


@login_manager.request_loader
def request_loader(request) -> None:
    return

@flask_app.route("/")
def home() -> Any:
    return render_template("home/home.html")


@flask_app.errorhandler(status.HTTP_403_FORBIDDEN)
def forbidden(e: Forbidden):
    return {
        "message": "Forbidden",
        "error": str(e),
    }, status.HTTP_403_FORBIDDEN


@flask_app.errorhandler(status.HTTP_404_NOT_FOUND)
def notfound(e: NotFound) -> Tuple[Dict[str, str], Literal[404]]:
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
    createsuperuserCli()


@click.command(name="test")
@with_appcontext
def test() -> None:
    """Runs the unit tests."""
    testCli()


flask_app.cli.add_command(createsuperuser)
flask_app.cli.add_command(test)
