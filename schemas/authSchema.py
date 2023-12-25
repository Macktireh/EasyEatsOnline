from flask_restx import Namespace, fields


class AuthSchema:
    api = Namespace("Auth", description="auth related operations")

    email = api.model(
        "email",
        {
            "email": fields.String(required=True, description="user email address"),
        },
    )

    login = api.clone(
        "login",
        email,
        {
            "email": fields.String(required=True, description="user email address"),
            "password": fields.String(required=True, description="user password"),
        },
    )

    signup = api.clone(
        "signup",
        login,
        {
            "firstName": fields.String(required=True, description="user firstname"),
            "lastName": fields.String(required=True, description="user lastname"),
            "passwordConfirm": fields.String(required=True, description="user password confirm"),
        },
    )

    resetPassword = api.model(
        "resetPassword",
        {
            "password": fields.String(required=True, description="user password"),
            "passwordConfirm": fields.String(required=True, description="user password confirm"),
        },
    )

    token = api.model(
        "token",
        {
            "token": fields.String(required=True, description="token"),
        },
    )
