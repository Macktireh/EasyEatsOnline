import jwt

from datetime import datetime, timedelta

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token

from config.settings import GlobalConfig
from models.types import TokenIdentityType, UserType
from models.user import User
from utils import status, validators


class AuthServices:
    
    @staticmethod
    def register(data: UserType):
        """Register a new user and send an email with an account activation link"""
        user = User.getByEmail(data.get('email'))
        if not user:
            if not validators.check_password_and_passwordConfirm(data.get('password'), data.get('passwordConfirm')):
                response_object = {
                    'status': "Fail",
                    'message': "Password and Confirm Password doesn't match."
                    }
                return response_object, status.HTTP_400_BAD_REQUEST
            is_validated = validators.validate_user(**data)
            if is_validated is not True:
                return dict(status="Fail", message='Invalid data', errors=is_validated), status.HTTP_400_BAD_REQUEST
            try:
                data1 = data.copy()
                data.pop('passwordConfirm', None)
                data.pop('sendMail', None)
                new_user = User.create(**data)
            except:
                return {
                    "message": "Something went wrong!",
                }, status.HTTP_500_INTERNAL_SERVER_ERROR
            
            if not data1.get('sendMail') == False:
                from utils.mail import send_email
                token = new_user.generateAccessToken()
                subject = "Please confirm your email"
                send_email(new_user, subject, template='mail/activate.html', domain=app.config["DOMAIN_FRONTEND"], token=token)
            
            response_object = {
                'status': 'success',
                'message': "User successfully created."
            }
            return response_object, status.HTTP_201_CREATED
        else:
            response_object = {
                'status': "Fail",
                'message': "User already exists. Please Log in.",
            }
            return response_object, status.HTTP_409_CONFLICT
    
    @staticmethod
    def activation(data: dict):
        user = User.checkAccessToken(data.get('token'))
        if user is not None:
            if not user.isActive:
                user.isActive = True
                user.updated = datetime.now()
                user.save()
                
                if not data.get('sendMail') == False:
                    from utils.mail import send_email
                    subject = "Your account is confirmed successfully"
                    send_email(user, subject, template='mail/activate_success.html')
                
                return {"status":'success', "message":'You have confirmed your account. Thanks!'}, status.HTTP_200_OK
            return {"status":'success', "message":'Account already confirmed. Please login.'}, status.HTTP_200_OK
        return {"status":"Fail", "message":'The confirmation link is invalid or has expired.'}, status.HTTP_400_BAD_REQUEST
    
    @staticmethod
    def encode_auth_token(user: User) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'publicId': user.publicId,
            'isAdmin': user.isAdmin,
        }
        return jwt.encode(payload, GlobalConfig.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def decode_auth_token(token: str) -> User:
        payload = jwt.decode(token, GlobalConfig.SECRET_KEY, algorithms=["HS256"])
        return User.getByPublicId(payload.get('publicId'))
    
    @staticmethod
    def login(email: str, password: str):
        is_validated = validators.validate_email_and_password(email, password)
        if is_validated is not True:
            return dict(status="fail", message='Invalid data', errors=is_validated), status.HTTP_400_BAD_REQUEST
        user = User.authenticate(email, password)
        if not user:
            res = {
                    'status': "Fail",
                    'message': 'Invalid email or password.'
                }
            return res, status.HTTP_400_BAD_REQUEST
        if not user.isActive:
            return {"status":"Fail", "message": 'Please confirm your account!'}, status.HTTP_403_FORBIDDEN
        try:
            access = create_access_token(identity={'publicId': user.publicId, 'isActive': user.isActive})
            refresh = create_refresh_token(identity={'publicId': user.publicId, 'isActive': user.isActive})
            return {
                'status': 'success',
                "message": "Successfully logged in.",
                "tokens": {
                    "access": access, "refresh": refresh
                }
            }, status.HTTP_200_OK
        except Exception as e:
            return {
                "error": "Something went wrong",
                "message": str(e)
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def refreshToken(identity: TokenIdentityType):
        user = User.getByPublicId(identity['publicId'])
        if user is not None:
            new_access = create_access_token(identity=identity)
            return {
                'status': 'success',
                "message": "Successfully logged in.",
                "access": new_access
            }, status.HTTP_200_OK
        return {
                'status': "Fail",
                "message": "The refresh token is invalid or has expired.",
                "code": "token_not_valid"
            }, status.HTTP_401_UNAUTHORIZED