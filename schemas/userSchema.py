from flask_restx import Namespace, fields


class UserSchema:
    api = Namespace("User", description="user related operations")

    User = api.model(
        "users",
        {
            "publicId": fields.String(description="user Identifier"),
            "email": fields.String(required=True, description="user email address"),
            "firstName": fields.String(required=True, description="user firstname"),
            "lastName": fields.String(required=True, description="user lastname"),
        },
    )
