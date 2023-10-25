import re
from typing import Any, Dict, Literal


REGEX_EMAIL_VALIDATION = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
REGEX_PASSWORD_VALIDATION = (
    r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
)
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
        return True if re.match(regex, field) else False

    @classmethod
    def validatePassword(cls, password: str) -> bool:
        """
        Validate the given password.

        Parameters:
            - password (str): The password to be validated.

        Returns:
            - bool: True if the password is valid, False otherwise.
        """
        return cls.validate(REGEX_PASSWORD_VALIDATION, password)

    @classmethod
    def validateEmail(cls, email: str) -> bool:
        """
        Validates an email address using a regular expression pattern.

        Args:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        return cls.validate(REGEX_EMAIL_VALIDATION, email)

    @classmethod
    def validateSignup(cls, **args: Dict[str, Any]) -> dict | Literal[True]:
        """
        Validate the signup data provided.

        Parameters:
            args (Dict[str, Any]): A dictionary containing the signup data.

        Returns:
            Union[Dict[str, str], Literal[True]]: Returns a dictionary of validation errors if there are any,
            otherwise returns True if the signup data is valid.
        """
        errors = {}

        required_fields = ["email", "password", "firstName", "lastName"]
        for field in required_fields:
            if not args.get(field):
                errors[field] = f"{field.capitalize()} is required"

        string_fields = ["email", "password"]
        for field in string_fields:
            if not isinstance(args.get(field), str):
                errors[field] = f"{field.capitalize()} must be a string"

        if "email" in args and not cls.validateEmail(args["email"]):
            errors["email"] = "Email is invalid"

        if "password" in args and not cls.validatePassword(args["password"]):
            errors["password"] = MESSAGE_PASSWORD_INVALID

        if "passwordConfirm" in args and not cls.checkPasswordAndPasswordConfirm(
            password=args["password"], passwordConfirm=args["passwordConfirm"]
        ):
            errors["passwordConfirm"] = "Password and Confirm Password doesn't match"

        if errors:
            return errors

        return True

    @staticmethod
    def validateLogin(email: str, password: str) -> dict | Literal[True]:
        """
        Validates a login by checking if the email and password are provided.

        Parameters:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            dict | Literal[True]: If there are any validation errors, a dictionary containing the errors. Otherwise,
            returns True.
        """
        errors = {}
        if not email:
            errors["email"] = "Email is required"
        if not password:
            errors["password"] = "Password is required"
        return errors or True

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
