from flask_restplus import Api
from flask import Blueprint

from .auth_controller import api as auth_api
from .user_controller import api as user_api
from .product_controller import api as product_api

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint,
        title='API REST Credit Cards',
        version='1.0',
        description='a boilerplate for flask restplus web service'
    )

api.add_namespace(auth_api, path='/auth/user')
api.add_namespace(user_api, path='/users')
api.add_namespace(product_api, path='/products')