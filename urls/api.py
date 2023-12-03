from flask import Blueprint
from flask_restx import Api

from controllers.authController import api as authApi
from controllers.cartController import api as cartApi
from controllers.categoryController import api as categoryApi
from controllers.orderController import api as orderApi
from controllers.productController import api as productApi
from controllers.userController import api as userApi

router = Blueprint("api", __name__, url_prefix="/api")


api = Api(
    router,
    version="1.0",
    title="EasyEatsOnline REST API",
    description="EasyEatsOnline API documentation for developers to use it.",
    doc="/docs",
    terms_url="https://www.google.com",
)

api.add_namespace(authApi, path="/auth/user")
api.add_namespace(userApi, path="/users")
api.add_namespace(categoryApi, path="/categories")
api.add_namespace(productApi, path="/products")
api.add_namespace(cartApi, path="/cart")
api.add_namespace(orderApi, path="/orders")
