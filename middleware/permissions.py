from functools import wraps

from flask_jwt_extended import get_jwt_identity
from werkzeug import exceptions

from services.userService import UserService


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        identity = get_jwt_identity()
        user = UserService.getUser(identity["publicId"])

        if not user.isAdmin or not user.isStaff:
            raise exceptions.Forbidden("You're not allowed to access this resource!")

        return f(*args, **kwargs)

    return decorated


def staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        identity = get_jwt_identity()
        user = UserService.getUser(identity["publicId"])

        if not user.isStaff:
            raise exceptions.Forbidden("You're not allowed to access this resource!")

        return f(*args, **kwargs)

    return decorated
