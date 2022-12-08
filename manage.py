import os
import click

from typing import Any, Dict, Literal, Union
from werkzeug.exceptions import NotFound, Forbidden

from flask import render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.cli import with_appcontext
from flask_admin.menu import MenuLink

from app import create_app, db
from services.user_service import UserServices
from utils import status
from utils.commandCLI import createsuperuser_cli, test_cli

# models
from models.user import User
from models.product import Product
from models.category import Category

# Admin
from admin.user import UserAdmin
from admin.product import ProductAdmin
from admin.category import CategoryAdmin

# routes
from admin.auth.login import admin_login
from controllers import blueprint as blueprint_api


# create app flask
flask_app, admin = create_app(os.environ.get('ProductionConfig', 'dev'))
migrate = Migrate(flask_app, db)

# save models in the admin panel
admin.add_view(UserAdmin(User, db.session))
admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(CategoryAdmin(Category, db.session))

# add menu items in the admin panel
admin.add_link(MenuLink(name='API Doc', category='', url="/api"))
admin.add_link(MenuLink(name='Logout', category='', url="/admin/user/logout"))

# register api routes
flask_app.register_blueprint(blueprint_api)
flask_app.register_blueprint(admin_login)

# flask login configuration
login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'admin.login'


@login_manager.user_loader
def user_loader(id: Union[str, int]) -> User:
    return UserServices.get_by_id(int(id))

@login_manager.request_loader
def request_loader(request) -> None:
    return

@flask_app.route('/')
def home() -> Any:
    return render_template('home/home.html') 

@flask_app.errorhandler(status.HTTP_403_FORBIDDEN)
def forbidden(e: Forbidden) -> tuple[Dict[str, str], Literal[403]]:
    return {
        "message": "Forbidden",
        "error": str(e),
    }, status.HTTP_403_FORBIDDEN

@flask_app.errorhandler(status.HTTP_404_NOT_FOUND)
def forbidden(e: NotFound) -> tuple[Dict[str, str], Literal[404]]:
    return {
        "message": "Endpoint Not Found",
        "error": str(e),
    }, status.HTTP_404_NOT_FOUND



@click.command(name='createsuperuser')
@with_appcontext
def createsuperuser() -> None:
    """Create a super user"""
    createsuperuser_cli(UserServices)

@click.command(name='test')
@with_appcontext
def test() -> None:
    """Runs the unit tests."""
    test_cli()

flask_app.cli.add_command(createsuperuser)
flask_app.cli.add_command(test)