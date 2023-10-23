from typing import Dict

from datetime import datetime

from flask import current_app as app, render_template
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import abort

from dto import RequestActivateDTO, RequestLoginDTO, RequestSignupDTO, TokenPayload
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
        """
        Registers a new user with the provided data.

        Args:
            data (RequestSignupDTO): The data for the user registration.

        Returns:
            Dict[str, str]: A dictionary containing the message indicating a successful registration.
        """
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

        body = render_template(
            "mail/activate.html",
            user=new_user,
            domain=app.config["DOMAIN_FRONTEND"],
            token=TokenService.generate(new_user),
        )
        EmailService.sendEmail(email=new_user.email, subject="Please confirm your email", body=body)

        return dict(message="You have registered successfully.")

    @staticmethod
    def activation(data: RequestActivateDTO) -> Dict[str, str]:
        """
        Verify the user's token and activate the user's account if it is not already active.

        Parameters:
            data (RequestActivateDTO): A dictionary containing the user's token.

        Returns:
            dict: A dictionary containing a message indicating the result of the activation process.
        """
        user = TokenService.verify(data["token"])
        if user is None:
            abort(status.HTTP_422_UNPROCESSABLE_ENTITY, message="Invalid token")

        if not user.isActive:
            user.isActive = True
            user.updated = datetime.now()
            userRepository.save(user)

            body = render_template("mail/activate_success.html", user=user)
            EmailService.sendEmail(email=user.email, subject="Your account is confirmed successfully", body=body)

            return dict(message="Account confirmed successfully")

        return abort(
            status.HTTP_410_GONE, message="Account already confirmed. Please login."
        )

    @classmethod
    def login(cls, data: RequestLoginDTO) -> Dict[str, str | Dict[str, str]] | None:
        """
        Logs in a user using the provided credentials.

        Args:
            data (RequestLoginDTO): The login credentials provided by the user.

        Returns:
            Union[Dict[str, str | Dict[str, str]], None]: If the login is successful,
            a dictionary containing a success message and the access and refresh tokens.
            If the login fails, None is returned.

        Raises:
            HTTPException: If the provided login information is not valid, an HTTP 400 Bad Request is raised.
            HTTPException: If the email address or password is invalid, an HTTP 401 Unauthorized is raised.
            HTTPException: If the user's account is not active, an HTTP 401 Unauthorized is raised.
            HTTPException: If an unexpected error occurs, an HTTP 500 Internal Server Error is raised.
        """
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
        """
        Refreshes the user token.

        Args:
            identity (TokenPayload): The user identity.

        Returns:
            Dict[str, str]: A dictionary containing the message and the refreshed access token.

        Raises:
            HTTPException: If the user is not authorized.

        """
        user = userRepository.getByPublicId(identity["publicId"])
        if user:
            return dict(
                message="Successfully refreshed.",
                access=create_access_token(identity=identity),
            )
        return abort(status.HTTP_401_UNAUTHORIZED, message="Invalid token")

    @staticmethod
    def authenticate(email: str, password: str) -> User | None:
        """
        Authenticates a user based on their email and password.

        Parameters:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User | None: If the email and password are valid, returns the authenticated user. Otherwise, returns None.
        """
        user = userRepository.getByEmail(email)
        if user and user.checkPassword(password):
            return user
        return None
