import jwt

from typing import Any, Dict, Union
from datetime import datetime

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token

from config.settings import GlobalConfig
from models.user import User
from utils import status, validators


class AuthServices:
    def __init__(self) -> None:
        return
    
    @staticmethod
    def register(data: dict[str, str]):
        """Register a new user and send an email with an account activation link"""
        user = User.getByEmail(data.get('email'))
        if not user:
            if not validators.check_password_and_passwordConfirm(data.get('password'), data.get('passwordConfirm')):
                response_object = {
                    'status': 'fail',
                    'message': "Password and Confirm Password doesn't match."
                    }
                return response_object, status.HTTP_400_BAD_REQUEST
            is_validated = validators.validate_user(**data)
            if is_validated is not True:
                return dict(status='fail', message='Invalid data', error=is_validated), status.HTTP_400_BAD_REQUEST
            try:
                data.pop('passwordConfirm', None)
                new_user = User.create(**data)
            except:
                return {
                    "message": "Something went wrong!",
                }, status.HTTP_500_INTERNAL_SERVER_ERROR
            
            from utils.mail import send_email
            token = new_user.generateAccessToken()
            subject = "Please confirm your email"
            send_email(new_user, subject, template='mail/activate.html', domain=app.config["DOMAIN_FRONTEND"], token=token)
            
            response_object = {
                'status': 'success',
                'message': "Successfully registered."
            }
            return response_object, status.HTTP_201_CREATED
        else:
            response_object = {
                'status': 'fail',
                'message': "User already exists. Please Log in.",
            }
            return response_object, status.HTTP_409_CONFLICT
    
    @staticmethod
    def activation(token: str):
        user = User.checkAccessToken(token)
        if user is not None:
            if not user.isActive:
                user.isActive = True
                user.updated = datetime.now()
                user.save()
                
                from utils.mail import send_email
                subject = "Your account is confirmed successfully"
                send_email(user, subject, template='mail/activate_success.html')
                
                return {"status":'success', "message":'You have confirmed your account. Thanks!'}, status.HTTP_200_OK
            else:
                return {"status":'success', "message":'Account already confirmed. Please login.'}, status.HTTP_200_OK
        else:
            return {"status":'fail', "message":'The confirmation link is invalid or has expired.'}, status.HTTP_400_BAD_REQUEST
    
    @staticmethod
    def encode_auth_token(user: User) -> str:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'publicId': user.publicId,
            'isAdmin': user.isAdmin,
        }
        return jwt.encode(payload, GlobalConfig.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def decode_auth_token(token: str) -> User:
        data = jwt.decode(token, GlobalConfig.SECRET_KEY, algorithms=["HS256"])
        return User.getByPublicId(data.sub.publicId)
    
    @staticmethod
    def login(email: str, password: str):
        is_validated = validators.validate_email_and_password(email, password)
        if is_validated is not True:
            return dict(status="fail", message='Invalid data', error=is_validated), status.HTTP_400_BAD_REQUEST
        user = User.authenticate(email, password)
        if not user:
            res = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
            return res, status.HTTP_403_FORBIDDEN
        if not user.isActive:
            return {"status":'fail', "message":'Please confirm your account!'}, status.HTTP_403_FORBIDDEN
        try:
            access = create_access_token(identity={'publicId': user.publicId, 'isAdmin': user.isAdmin})
            refresh = create_refresh_token(identity={'publicId': user.publicId, 'isAdmin': user.isAdmin})
            return {
                'status': 'success',
                "message": "Successfully fetched auth token",
                "tokens": {
                    "access": access, "refresh": refresh
                }
            }
        except Exception as e:
            return {
                "error": "Something went wrong",
                "message": str(e)
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def refreshToken(identity: Any):
        user = User.getByPublicId(identity['publicId'])
        if user is not None:
            new_access = create_access_token(identity=identity)
            return {"access": new_access}, status.HTTP_200_OK
        return {
                'status': 'fail',
                "message": "The token is invalid or expired",
                "code": "token_not_valid"
            }, status.HTTP_401_UNAUTHORIZED