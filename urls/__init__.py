from flask import Blueprint

from urls.api import router as routerApi
from urls.web import router as routerWeb

routes = Blueprint("app", __name__)

routes.register_blueprint(routerApi)
routes.register_blueprint(routerWeb)
