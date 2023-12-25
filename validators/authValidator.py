import re
from typing import Any, Dict, Literal

from flask_restx import abort

from utils import status

REGEX_EMAIL_VALIDATION = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
REGEX_PASSWORD_VALIDATION = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
MESSAGE_PASSWORD_INVALID = "Password is invalid, Should be atleast 8 characters with upper and lower case letters, numbers and special characters"  # noqa


class AuthValidator:
    """
    A class for validating data using regular expressions.
    """

    @staticmethod
    def validate(regex: Literal, field: str) -> bool:
        """
        Validate if a given field matches a specified regular expression pattern.

        Args:
            regex (Literal): The regular expression pattern to match against.
            field (str): The field to be validated.

        Returns:
            bool: True if the field matches the pattern, False otherwise.
        """
        return bool(re.match(regex, field))

    @staticmethod
    def validatePassword(password: str) -> bool:
        """
        Validate the given password.

        Parameters:
            - password (str): The password to be validated.

        Returns:
            - bool: True if the password is valid, False otherwise.
        """
        return AuthValidator.validate(REGEX_PASSWORD_VALIDATION, password)

    @staticmethod
    def validateEmail(email: str) -> bool:
        """
        Validates an email address using a regular expression pattern.

        Args:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        return AuthValidator.validate(REGEX_EMAIL_VALIDATION, email)

    @staticmethod
    def validateSignupRaise(**kwargs: Dict[str, Any]) -> Literal[True]:
        """
        Validate the signup data provided.

        Parameters:
            kwargs (Dict[str, Any]): A dictionary containing the signup data.

        Returns:
            Union[Dict[str, str], Literal[True]]: Returns a dictionary of validation errors if there are any,
            otherwise returns True if the signup data is valid.
        """
        errors = {}

        required_fields = ["email", "password", "firstName", "lastName"]
        for field in required_fields:
            if not kwargs.get(field):
                errors[field] = f"{field.capitalize()} is required"

        string_fields = ["email", "password"]
        for field in string_fields:
            if not isinstance(kwargs.get(field), str):
                errors[field] = f"{field.capitalize()} must be a string"

        if "email" in kwargs and not AuthValidator.validateEmail(kwargs["email"]):
            errors["email"] = "Email is invalid"

        if "password" in kwargs and not AuthValidator.validatePassword(kwargs["password"]):
            errors["password"] = MESSAGE_PASSWORD_INVALID

        if "passwordConfirm" in kwargs and not AuthValidator.checkPasswordAndPasswordConfirm(
            password=kwargs["password"], passwordConfirm=kwargs["passwordConfirm"]
        ):
            errors["passwordConfirm"] = "Password and Confirm Password doesn't match"

        if errors:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=errors,
            )

        return True

    @staticmethod
    def validateLoginRaise(**kwargs: Dict[str, Any]) -> Literal[True]:
        """
        Validates the login credentials provided by the user.

        Args:
            kwargs (Dict[str, Any]): A dictionary containing the login credentials.
        Returns:
            True: If the login credentials are valid.

        Raises:
            HTTPException: If the email or password is missing.
        """
        errors = {}
        required_fields = ["email", "password"]
        for field in required_fields:
            if not kwargs.get(field):
                errors[field] = f"{field.capitalize()} is required"

        if errors:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=errors,
            )
        return True

    @staticmethod
    def validateEmailRaise(email: str) -> Literal[True]:
        """
        Validate the request to reset the password.

        Args:
            email (str): The email address of the user.

        Returns:
            True: If the request is valid.

        Raises:
            HTTPException: If the request is not valid.

        """
        errors = {}

        if not email:
            errors["email"] = "Email is required"

        if not AuthValidator.validateEmail(email):
            errors["email"] = "Email is invalid"

        if errors:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=errors,
            )

        return True

    @staticmethod
    def validateResetPasswordRaise(**kwargs: Dict[str, Any]) -> Literal[True]:
        """
        Validate the reset password data provided.

        Parameters:
            kwargs (Dict[str, Any]): A dictionary containing the reset password data.

        Returns:
            Union[Dict[str, str], Literal[True]]: Returns a dictionary of validation errors if there are any,
            otherwise returns True if the reset password data is valid.
        """
        errors = {}

        required_fields = ["password", "passwordConfirm"]
        for field in required_fields:
            if not kwargs.get(field):
                errors[field] = f"{field.capitalize()} is required"

        if "password" in kwargs and not AuthValidator.validatePassword(kwargs["password"]):
            errors["password"] = MESSAGE_PASSWORD_INVALID

        if "passwordConfirm" in kwargs and not AuthValidator.checkPasswordAndPasswordConfirm(
            password=kwargs["password"], passwordConfirm=kwargs["passwordConfirm"]
        ):
            errors["passwordConfirm"] = "Password and Confirm Password doesn't match"

        if errors:
            abort(
                status.HTTP_400_BAD_REQUEST,
                message="The information provided is not valid",
                errors=errors,
            )

        return True

    @staticmethod
    def checkPasswordAndPasswordConfirm(password: str, passwordConfirm: str) -> bool:
        """
        Check if the given password and password confirmation match.

        Args:
            password (str): The password to be checked.
            passwordConfirm (str): The password confirmation.

        Returns:
            bool: True if the password and password confirmation match, False otherwise.
        """
        return password == passwordConfirm
