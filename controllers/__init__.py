from flask_restplus import Api
from flask import Blueprint

from controllers.auth_controller import api as auth_api
from controllers.user_controller import api as user_api
from controllers.product_controller import api as product_api
from controllers.category_controller import api as category_api


blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint,
        title='API REST Credit Cards',
        version='1.0',
        description='a boilerplate for flask restplus web service'
    )

api.add_namespace(auth_api, path='/auth/user')
api.add_namespace(user_api, path='/users')
api.add_namespace(product_api, path='/products')
api.add_namespace(category_api, path='/categories')