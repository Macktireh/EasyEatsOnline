from typing import Dict

from datetime import datetime

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import abort

from dto import RequestLoginDTO, RequestSignupDTO, TokenPayload
from models.user import User
from repository.userRepository import userRepository
from services.emailService import EmailService
from services.tokenService import TokenService
from utils import status
from utils.validators import validator


class AuthService:
    """Handles authentication and authorization."""

    @staticmethod
    def register(data: RequestSignupDTO) -> Dict[str, str]:
        user = userRepository.getByEmail(data["email"])
        if user:
            abort(status.HTTP_409_CONFLICT, message="User already exists")

        validated = validator.validateSignup(**data)
        if validated is not True:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=validated,
            )

        data.pop("passwordConfirm", None)
        new_user = userRepository.create(**data)

        from utils.mail import send_email

        send_email(
            user=new_user,
            subject="Please confirm your email",
            template="mail/activate.html",
            domain=app.config["DOMAIN_FRONTEND"],
            token=TokenService.generate(new_user),
        )

        return dict(message="You have registered successfully.")

    @staticmethod
    def activation(data: dict) -> Dict[str, str]:
        user = TokenService.verify(data["token"])
        if user is None:
            abort(status.HTTP_422_UNPROCESSABLE_ENTITY, message="Invalid token")

        if not user.isActive:
            user.isActive = True
            user.updated = datetime.now()
            userRepository.save(user)

            from utils.mail import send_email

            subject = "Your account is confirmed successfully"
            send_email(user, subject, template="mail/activate_success.html")

            return dict(message="Account confirmed successfully")

        return abort(
            status.HTTP_410_GONE, message="Account already confirmed. Please login."
        )

    @classmethod
    def login(cls, data: RequestLoginDTO) -> Dict[str, str | Dict[str, str]] | None:
        validated = validator.validateLogin(**data)
        if validated is not True:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=validated,
            )

        user = cls.authenticate(**data)
        if not user:
            abort(
                status.HTTP_401_UNAUTHORIZED,
                message="Invalid email address or password",
            )

        if not user.isActive:
            abort(status.HTTP_401_UNAUTHORIZED, message="Your account is not active")

        try:
            identity = {"publicId": user.publicId, "isActive": user.isActive}
            access = create_access_token(identity=identity)
            refresh = create_refresh_token(identity=identity)
            return dict(
                message="Successfully logged in.",
                tokens={"access": access, "refresh": refresh},
            )
        except Exception as e:
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR, message="Something went wrong")

    @staticmethod
    def refreshToken(identity: TokenPayload) -> Dict[str, str]:
        user = userRepository.getByPublicId(identity["publicId"])
        if user:
            return dict(
                message="Successfully refreshed.",
                access=create_access_token(identity=identity),
            )
        return abort(status.HTTP_401_UNAUTHORIZED, message="Invalid token")

    @staticmethod
    def authenticate(email: str, password: str) -> User | None:
        user = userRepository.getByEmail(email)
        if user and user.checkPassword(password):
            return user
        return None
