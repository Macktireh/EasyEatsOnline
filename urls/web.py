from flask import Blueprint

from controllers.adminAuthController import router as routerAdminLogin
from controllers.homeController import router as routerHome

router = Blueprint("web", __name__)

router.register_blueprint(routerAdminLogin)
router.register_blueprint(routerHome)
