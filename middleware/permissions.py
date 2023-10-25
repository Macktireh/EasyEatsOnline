from functools import wraps
from werkzeug import exceptions
from flask_jwt_extended import get_jwt_identity

from services.userService import UserService
from utils import status


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        identity = get_jwt_identity()
        user = UserService.getUser(identity["publicId"])

        if not user.isAdmin and not user.isStaff:
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
