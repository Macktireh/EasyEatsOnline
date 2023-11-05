from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from schemas.authSchema import AuthSchema
from services.authService import AuthService
from utils import status

api = AuthSchema.api


@api.route("/signup")
class SignupController(Resource):
    @api.response(status.HTTP_201_CREATED, "User successfully created.")
    @api.doc("create a new user")
    @api.expect(AuthSchema.signup, validate=True)
    def post(self):
        """Creates a new User"""
        return AuthService.register(request.json), status.HTTP_201_CREATED


@api.route("/activation")
class ActivationController(Resource):
    @api.response(status.HTTP_200_OK, "Account Activation successfully.")
    @api.doc("Account Activation")
    @api.expect(AuthSchema.token, validate=True)
    def post(self):
        """Account Activation"""
        return AuthService.activation(request.json)


@api.route("/login")
class LoginController(Resource):
    @api.response(status.HTTP_200_OK, "User successfully login.")
    @api.doc("user login")
    @api.expect(AuthSchema.login, validate=True)
    def post(self):
        """User Login"""
        return AuthService.login(request.json)


@api.route("/token/refresh")
class RefreshTokenController(Resource):
    @api.response(status.HTTP_200_OK, "Refresh Token JWT")
    @api.doc("Refresh Token JWT")
    @jwt_required(refresh=True)
    def post(self):
        """Refresh JWT token"""
        identity = get_jwt_identity()
        return AuthService.refreshToken(identity)
