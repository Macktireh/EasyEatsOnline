from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.userSchema import UserSchema
from services.userService import UserService


api = UserSchema.api


@api.route("/me")
class RetrieveUpdateCurrentUserController(Resource):
    @api.doc("get_current_user")
    @api.marshal_list_with(UserSchema.user, envelope="data")
    @jwt_required()
    def get(self):
        """Get Current User"""
        identity = get_jwt_identity()
        return UserService.getUser(identity["publicId"])

    @api.doc("update_current_user")
    @api.marshal_list_with(UserSchema.user, envelope="data")
    @jwt_required()
    def patch(self):
        """Update Current User"""
        identity = get_jwt_identity()
        return UserService.updateUser(publicId=identity["publicId"], data=request.json)


@api.route("")
class ListUserController(Resource):
    @api.doc("list_of_registered_users")
    @api.marshal_list_with(UserSchema.user, envelope="data")
    @jwt_required()
    def get(self):
        """List all registered users"""
        return UserService.getAllUser()
