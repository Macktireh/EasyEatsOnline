from functools import wraps
from flask import request, abort
from flask_jwt_extended import decode_token

from services.user_service import UserServices
from utils import status
from utils.token import check_access_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("token_required")
        token = None
        print(request.headers["Authorization"])
        if "Authorization" in request.headers:
            authorization = request.headers["Authorization"].split(" ")
            if "bearer" != authorization[0].lower() or len(authorization) != 2:
                return {
                    "message": "Authentication Token is missing!",
                    "error": "Unauthorized"
                }, status.HTTP_401_UNAUTHORIZED
            token = authorization[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "error": "Unauthorized"
            }, status.HTTP_401_UNAUTHORIZED
        try:
            current_user = check_access_token(token)
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "error": "Unauthorized"
            }, status.HTTP_401_UNAUTHORIZED
            # if not current_user.isActive:
            #     abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "error": str(e)
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
        return f(current_user, *args, **kwargs)
    return decorated