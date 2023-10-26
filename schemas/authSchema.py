from flask_restx import Namespace, fields


class AuthSchema:
    api = Namespace("Auth", description="user auth")

    login = api.model(
        "login",
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
            "passwordConfirm": fields.String(
                required=True, description="user password confirm"
            ),
        },
    )

    token = api.model(
        "token",
        {
            "token": fields.String(required=True, description="token"),
        },
    )
