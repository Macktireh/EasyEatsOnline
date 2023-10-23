from flask_restx import Namespace, fields


class authSchema:
    api = Namespace("Auth", description="user auth")

    Login = api.model(
        "login",
        {
            "email": fields.String(required=True, description="user email address"),
            "password": fields.String(required=True, description="user password"),
        },
    )

    Signup = api.clone(
        "signup",
        Login,
        {
            "firstName": fields.String(required=True, description="user firstname"),
            "lastName": fields.String(required=True, description="user lastname"),
            "publicId": fields.String(description="user Identifier"),
            "passwordConfirm": fields.String(
                required=True, description="user password confirm"
            ),
        },
    )

    Token = api.model(
        "token",
        {
            "token": fields.String(required=True, description="token"),
        },
    )
