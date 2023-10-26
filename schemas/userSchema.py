from flask_restx import Namespace, fields


class UserSchema:
    api = Namespace("User", description="user related operations")

    user = api.model(
        "user",
        {
            "publicId": fields.String(description="user Identifier"),
            "email": fields.String(required=True, description="user email address"),
            "firstName": fields.String(required=True, description="user firstname"),
            "lastName": fields.String(required=True, description="user lastname"),
        },
    )

    userDetail = api.clone(
        "userDetail",
        user,
        {
            "isActive": fields.Boolean(required=False, description="user is active"),
            "isStaff": fields.Boolean(required=False, description="user is staff"),
            "isAdmin": fields.Boolean(required=False, description="user is admin"),
        }
    )
