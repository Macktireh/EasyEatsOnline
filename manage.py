from typing import Any, Dict, Literal, Tuple, Union

import click
from flask import redirect, render_template, url_for
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

# from admin.register import registerAdmin
from app import createApp, db
from config.settings import getEnvVar
from controllers import apiRoute
from controllers.adminAuthController import adminLogin
from models.user import User
from repository.userRepository import userRepository
from utils import status
from utils.cli import createSuperUserCli, runTests

app = createApp(getEnvVar("FLASK_ENV", "development"))

migrate = Migrate(app, db)
# registerAdmin(app, db)

# register api routes
app.register_blueprint(apiRoute)
app.register_blueprint(adminLogin)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin.login"


@app.route("/")
def home() -> Any:
    return redirect(url_for("api.doc"))
    return render_template("home/home.html")


@login_manager.user_loader
def user_loader(id: Union[str, int]) -> User:
    return userRepository.getById(int(id))


@login_manager.request_loader
def request_loader(request) -> None:
    return


@app.errorhandler(status.HTTP_403_FORBIDDEN)
def forbidden(e: Forbidden) -> Tuple[Dict[str, str], Literal[403]]:
    return {
        "message": "Forbidden",
        "error": str(e),
    }, status.HTTP_403_FORBIDDEN


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def notfound(e: NotFound) -> Tuple[Dict[str, str], Literal[404]]:
    return {
        "message": "Endpoint Not Found",
        "error": str(e),
    }, status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
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
    runTests()


app.cli.add_command(createsuperuser)
app.cli.add_command(test)
