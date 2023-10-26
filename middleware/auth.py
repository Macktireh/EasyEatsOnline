from functools import wraps

from flask import request
from werkzeug import exceptions

from services.tokenService import TokenService


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if authorization_header:
            authorization = authorization_header.split(" ")
            if len(authorization) == 2 and authorization[0].lower() == "bearer":
                token = authorization[1]
        if not token:
            raise exceptions.Unauthorized("Authentication Token is missing!")
        current_user = TokenService.verify(token)
        if not current_user:
            raise exceptions.Unauthorized("Invalid token")
        return f(current_user, *args, **kwargs)

    return decorated
