from flask_restx import Api
from flask import Blueprint

from controllers.authCotroller import api as auth_api
from controllers.userController import api as user_api
# from controllers.product_routes import api as product_api
# from controllers.category_routes import api as category_api
# from controllers.cart_routes import api as cart_api
# from controllers.order_routes import api as order_api


blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    blueprint,
    version="1.0",
    title="Tech Shoping REST APIs",
    description="a boilerplate for flask restplus web service",
)

api.add_namespace(auth_api, path="/auth/user")
api.add_namespace(user_api, path="/users")
# api.add_namespace(product_api, path="/products")
# api.add_namespace(category_api, path="/categories")
# api.add_namespace(cart_api, path="/carts")
# api.add_namespace(order_api, path="/orders")
