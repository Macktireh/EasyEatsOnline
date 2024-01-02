from typing import Dict, Literal, Tuple, Union

import click
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from admin.register import registerAdmin
from config.app import createApp, db
from config.settings import ConfigName, getEnvVar
from models.user import User
from repository.userRepository import userRepository
from urls.api import router as routerApi
from urls.web import router as routerWeb
from utils import status
from utils.cli import createSuperUserCli, exportPostmanCollection, runTests

app = createApp(getEnvVar("FLASK_ENV", ConfigName.DEVELOPEMENT.value))

migrate = Migrate(app, db)
registerAdmin(app, db)

# routes registration
app.register_blueprint(routerApi)
app.register_blueprint(routerWeb)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin.login"


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
    """
    Create a super user.

    Usage:\n
        (create super user): flask createsuperuser
    """
    createSuperUserCli()


@click.command(name="test")
@click.option("--dir", type=click.STRING, default="tests", help="Test directory")
@click.option("--pattern", type=click.STRING, default="test*.py", help="Test pattern")
@click.option("--verbosity", type=click.INT, default=2, help="Test verbosity")
@with_appcontext
def test(dir: str, pattern: str, verbosity: int) -> None:
    """
    Run tests.

    Args:\n
        dir (str): Test directory.\n
        pattern (str): Test pattern.\n
        verbosity (int): Test verbosity.

    Usage:\n
        (run tests): flask test\n
        (run tests with directory and pattern): flask test --dir=tests/test_api --pattern=test*.py\n
        (run tests with verbose output): flask test --verbosity=2
    """
    runTests(dir, pattern, verbosity)


@app.cli.command(name="postman")
@click.option("--export", type=click.BOOL, default=False, help="Export Postman collection")
def postman(export: bool) -> None:
    """
    Generate the Postman collection for the application.

    Args:\n
        export (bool): A flag indicating whether to export the Postman collection.

    Usage:\n
        (printed collection): poetry run flask postman\n
        (exported collection to json): poetry run flask postman --export=True
    """
    exportPostmanCollection(export)


app.cli.add_command(createsuperuser)
app.cli.add_command(test)
