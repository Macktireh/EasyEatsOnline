from flask_restx import Api
from flask import Blueprint

from controllers.authController import api as authApi
from controllers.userController import api as userApi
from controllers.categoryController import api as categoryApi
from controllers.productController import api as productApi
from controllers.cartController import api as cartApi
from controllers.orderController import api as orderApi


apiRoute = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    apiRoute,
    version="1.0",
    title="Tech Shoping REST APIs",
    description="a boilerplate for flask restplus web service",
    doc="/docs",
)

api.add_namespace(authApi, path="/auth/user")
api.add_namespace(userApi, path="/users")
api.add_namespace(categoryApi, path="/categories")
api.add_namespace(productApi, path="/products")
api.add_namespace(cartApi, path="/cart")
api.add_namespace(orderApi, path="/orders")
