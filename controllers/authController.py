from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, reqparse

from schemas.authSchema import AuthSchema
from services.authService import AuthService
from utils import status

api = AuthSchema.api


@api.route("/signup")
class SignupController(Resource):
    @api.response(status.HTTP_201_CREATED, "User successfully created.")
    @api.doc("user signup")
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
    @api.response(status.HTTP_200_OK, "Refresh JWT token successfully.")
    @api.doc("Refresh JWT token")
    @jwt_required(refresh=True)
    def post(self):
        """Refresh JWT token"""
        identity = get_jwt_identity()
        return AuthService.refreshToken(identity)


@api.route("/request-password-reset")
class RequestPasswordResetController(Resource):
    @api.response(status.HTTP_200_OK, "Password reset link successfully sent.")
    @api.doc("Request Password Reset Link")
    @api.expect(AuthSchema.email, validate=True)
    def post(self):
        """Request Password Reset Link"""
        return AuthService.requestPasswordReset(request.json["email"])


@api.route("/reset-password/")
@api.param("token", "Password reset token")
class ResetPasswordController(Resource):
    @api.response(status.HTTP_200_OK, "Password reset successfully.")
    @api.doc("Reset Password")
    @api.expect(AuthSchema.resetPassword, validate=True)
    def post(self):
        """Reset Password"""
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, type=str, help="Password reset token")
        args = parser.parse_args()
        return AuthService.resetPassword(token=args["token"], data=request.json)


@api.route("/resend-activation-email")
class ResendActivationEmailController(Resource):
    @api.response(status.HTTP_200_OK, "Activation email successfully sent.")
    @api.doc("Resend Activation Email")
    @api.expect(AuthSchema.email, validate=True)
    def post(self):
        """Resend Activation Email"""
        return AuthService.resendConfirmationEmail(request.json["email"])
