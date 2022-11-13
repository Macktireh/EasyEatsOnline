import os
import click
from typing import Dict, Literal
from werkzeug.exceptions import NotFound, Forbidden

import flask_login
from flask import jsonify, render_template
from flask_migrate import Migrate
from flask.cli import with_appcontext
from flask_admin.menu import MenuLink

from app import create_app, db
from services.user_service import UserServices
from utils import status
from utils.commandCLI import createsuperuser_cli, test_cli

# models
from models.user import User, UserImage

# Admin
from admin.user import UserAdminModelView, UserImageAdminModelView

# routes
from admin.auth.login import admin_login
from controller import blueprint as blueprint_api

# create app flask
flask_app, admin = create_app(os.environ.get('BOILERPLATE_ENV', 'dev'))
migrate = Migrate(flask_app, db)

# Admin pannel register model
admin.add_view(UserAdminModelView(User, db.session))
admin.add_view(UserImageAdminModelView(UserImage, db.session))
# admin.add_menu_item
admin.add_link(MenuLink(name='API Doc', category='', url="/api"))
admin.add_link(MenuLink(name='Logout', category='', url="/admin/user/logout"))

# register api routes
flask_app.register_blueprint(blueprint_api)
flask_app.register_blueprint(admin_login)

# config flask login
login_manager = flask_login.LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'admin.login'


@login_manager.user_loader
def user_loader(id: str | int) -> User:
    return UserServices().get_by_id(int(id))

@login_manager.request_loader
def request_loader(request) -> None:
    return

@flask_app.route('/')
def home():
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

# add command function to cli commands
flask_app.cli.add_command(createsuperuser)
flask_app.cli.add_command(test)