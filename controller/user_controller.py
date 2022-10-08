from flask import request
from flask_restplus import Resource

from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.auth import token_required

from schemas.dto import UserDto
from services.user_service import UserServices
from utils import status


api = UserDto.api

@api.route('/me')
class CurrentUserRoute(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(UserDto.IUser, envelope='data')
    @jwt_required()
    def get(self):
        """List all registered users"""
        # return current_user
        identity = get_jwt_identity()
        return UserServices().get_by_publicId(identity["publicId"])
        # current_user = UserServices().get_by_publicId(identity["publicId"])
        # print()
        # print(current_user)
        # print()
        # if current_user is not None:
        #     return UserServices().get_by_publicId(identity["publicId"])
        # return {
        #         'status': 'fail',
        #         "message": "The token is invalid or expired",
        #         "code": "token_not_valid"
        #     }, status.HTTP_401_UNAUTHORIZED


# @api.route('/<publicId>')
# @api.param('publicId', 'The User identifier')
# @api.response(404, 'User not found.')
# class User(Resource):
#     @api.doc('get a user')
#     @api.marshal_with(UserDto.users)
#     def get(self, publicId):
#         """get a user given its identifier"""
#         user = get_a_user(publicId)
#         if not user:
#             api.abort(404)
#         else:
#             return user
