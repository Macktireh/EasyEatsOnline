from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from schemas.userSchema import UserSchema
from services.userService import UserService

api = UserSchema.api


@api.route("/me")
class RetrieveUpdateCurrentUserController(Resource):
    @api.doc("Get Current User")
    @api.marshal_list_with(UserSchema.user, envelope="data")
    @jwt_required()
    def get(self):
        """Get Current User"""
        identity = get_jwt_identity()
        return UserService.getUser(identity["publicId"])

    @api.doc("Update Current User")
    @api.marshal_list_with(UserSchema.user, envelope="data")
    @jwt_required()
    def patch(self):
        """Update Current User"""
        identity = get_jwt_identity()
        return UserService.updateUser(publicId=identity["publicId"], data=request.json)


@api.route("")
class ListUserController(Resource):
    @api.doc("List all registered users")
    @api.marshal_list_with(UserSchema.user, envelope="data")
    @jwt_required()
    def get(self):
        """List all registered users"""
        identity = get_jwt_identity()
        return UserService.getAllUsers(identity["publicId"])
