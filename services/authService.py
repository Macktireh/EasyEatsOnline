from typing import Dict

from datetime import datetime

from flask import current_app as app, render_template
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import abort
from werkzeug import exceptions

from dto import RequestActivateDTO, RequestLoginDTO, RequestSignupDTO, TokenPayload
from models.user import User
from repository.userRepository import userRepository
from services.emailService import EmailService
from services.tokenService import TokenService
from utils import status
from validators.authValidator import AuthValidator


class AuthService:
    """Handles authentication."""

    @staticmethod
    def register(data: RequestSignupDTO) -> Dict[str, str]:
        user = userRepository.getByEmail(data["email"])
        if user:
            raise exceptions.Conflict("User already exists")

        validated = AuthValidator.validateSignup(**data)
        if validated is not True:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=validated,
            )

        data.pop("passwordConfirm", None)
        new_user = userRepository.create(**data)

        body = render_template(
            "mail/activate.html",
            user=new_user,
            domain=app.config["DOMAIN_FRONTEND"],
            token=TokenService.generate(new_user),
        )
        EmailService.sendEmail(recipients=[new_user.email], subject="Please confirm your email", body=body)

        return dict(message="You have registered successfully.")

    @staticmethod
    def activation(data: RequestActivateDTO) -> Dict[str, str]:
        user = TokenService.verify(data["token"])
        if not user:
            raise exceptions.UnprocessableEntity("Invalid token")

        if not user.isActive:
            user.isActive = True
            user.updated = datetime.now()
            userRepository.save(user)

            body = render_template("mail/activate_success.html", user=user)
            EmailService.sendEmail(recipients=[user.email], subject="Your account is confirmed successfully", body=body)

            return dict(message="Account confirmed successfully")

        raise exceptions.Gone("Account already confirmed. Please login.")

    @classmethod
    def login(cls, data: RequestLoginDTO) -> Dict[str, str | Dict[str, str]] | None:
        validated = AuthValidator.validateLogin(**data)
        if validated is not True:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=validated,
            )

        user = cls.authenticate(**data)
        if not user:
            raise exceptions.Unauthorized("Invalid email address or password")

        if not user.isActive:
            raise exceptions.Unauthorized("Your account is not active")

        try:
            identity = {"publicId": user.publicId, "isActive": user.isActive}
            access = create_access_token(identity=identity)
            refresh = create_refresh_token(identity=identity)
            return dict(
                message="Successfully logged in.",
                tokens={"access": access, "refresh": refresh},
            )
        except Exception as e:
            raise exceptions.InternalServerError("Something went wrong")

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
    def authenticate(email: str, password: str) -> User | None:
        user = userRepository.getByEmail(email)
        if user and user.checkPassword(password):
            return user
        return None
