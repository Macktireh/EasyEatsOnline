from typing import Dict

from flask import current_app as app
from flask import render_template
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug import exceptions

from dto import RequestActivateDTO, RequestLoginDTO, RequestResetPasswordDTO, RequestSignupDTO, TokenPayload
from models.user import User
from repository.userRepository import userRepository
from services.emailService import EmailService
from services.tokenService import TokenService
from validators.authValidator import AuthValidator


class AuthService:
    TEMPLATE_ACTIVATION = "mail/activate.html"
    TEMPLATE_ACTIVATION_SUCCESS = "mail/activate_success.html"
    TEMPLATE_RESET_PASSWORD = "mail/reset_password.html"
    TEMPLATE_RESET_PASSWORD_SUCCESS = "mail/reset_password_success.html"

    @staticmethod
    def register(data: RequestSignupDTO) -> Dict[str, str]:
        if userRepository.existsByEmail(data["email"]):
            raise exceptions.Conflict("User already exists")

        AuthValidator.validateSignupRaise(**data)

        data.pop("passwordConfirm", None)
        user = userRepository.create(**data)
        AuthService.sendEmail("Please confirm your account", AuthService.TEMPLATE_ACTIVATION, user)

        return dict(message="You have registered successfully.")

    @staticmethod
    def activation(data: RequestActivateDTO) -> Dict[str, str]:
        user = TokenService.verify(data["token"])
        if not user:
            raise exceptions.UnprocessableEntity("Invalid token")

        if not user.isActive:
            user.isActive = True
            userRepository.save(user)

            if not app.config["TESTING"]:
                AuthService.sendEmail("Account confirmed successfully", AuthService.TEMPLATE_ACTIVATION_SUCCESS, user)

        return dict(message="Account confirmed successfully. Please login.")

    @staticmethod
    def login(data: RequestLoginDTO) -> Dict[str, str | Dict[str, str]] | None:
        AuthValidator.validateLoginRaise(**data)

        user = AuthService.authenticate(**data)
        if not user:
            raise exceptions.Unauthorized("Invalid email address or password")

        if not user.isActive:
            raise exceptions.Unauthorized("Your account is not active")

        access = create_access_token(identity={"publicId": user.publicId})
        refresh = create_refresh_token(identity={"publicId": user.publicId})
        return dict(message="Successfully logged in.", tokens={"access": access, "refresh": refresh})

    @staticmethod
    def refreshToken(identity: TokenPayload) -> Dict[str, str]:
        user = userRepository.getByPublicId(identity["publicId"])
        if not user:
            raise exceptions.Unauthorized("Invalid token")
        return dict(
            message="Successfully refreshed.",
            access=create_access_token(identity=identity),
        )

    @staticmethod
    def resendConfirmationEmail(email: str) -> None:
        AuthValidator.validateEmailRaise(email)
        user = userRepository.getByEmail(email)
        if user and not user.isActive:
            AuthService.sendEmail("Please confirm your account", AuthService.TEMPLATE_ACTIVATION, user)
        return dict(
            message="If the email exists, you will receive an email with instructions on how to confirm your account."
        )

    @staticmethod
    def requestPasswordReset(email: str) -> Dict[str, str]:
        AuthValidator.validateEmailRaise(email)
        user = userRepository.getByEmail(email)
        if user and user.isActive:
            AuthService.sendEmail("Reset your password", AuthService.TEMPLATE_RESET_PASSWORD, user)
        return dict(
            message="If the email exists, you will receive an email with instructions on how to reset your password."
        )

    @staticmethod
    def resetPassword(token: str, data: RequestResetPasswordDTO) -> Dict[str, str]:
        user = TokenService.verify(token, expiration=60 * 30)
        if not user:
            raise exceptions.UnprocessableEntity("Invalid token")

        AuthValidator.validateResetPasswordRaise(**data)

        user.password = data["password"]
        userRepository.save(user)
        AuthService.sendEmail(
            "Your password has been reset successfully", AuthService.TEMPLATE_RESET_PASSWORD_SUCCESS, user
        )
        return dict(message="Your password has been reset successfully.")

    @staticmethod
    def authenticate(email: str, password: str) -> User | None:
        user = userRepository.getByEmail(email)
        if user and user.checkPassword(password):
            return user
        return None

    @staticmethod
    def sendEmail(subject: str, template: str, user: User) -> None:
        if not app.config["TESTING"]:
            body = render_template(
                template_name_or_list=template,
                CLIENT_BASE_URL=app.config["CLIENT_BASE_URL"],
                token=TokenService.generate({"publicId": user.publicId, "isActive": user.isActive}),
                user=user,
            )
            EmailService.sendEmail(recipients=[user.email], subject=subject, body=body)
