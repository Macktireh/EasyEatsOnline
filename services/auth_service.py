import datetime
import jwt

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token

from config.settings import SECRET_KEY
from services.user_service import UserServices
from utils.token import generate_access_token, check_access_token
from utils import status, validators


class AuthServices:
    def __init__(self):
        return

    def register(self, data: dict):
        """Register a new user and send an email with an account activation link"""
        user = UserServices().get_by_email(data.get('email'))
        if not user:
            if not validators.validate_password_and_passwordConfirm_match(data.get('password'), data.get('passwordConfirm')):
                response_object = {
                    'status': 'fail',
                    'message': "Password and Confirm Password doesn't match."
                    }
                return response_object, status.HTTP_400_BAD_REQUEST
            is_validated = validators.validate_user(**data)
            if is_validated is not True:
                return dict(status='fail', message='Invalid data', error=is_validated), status.HTTP_400_BAD_REQUEST
            try:
                new_user = UserServices().create(data)
            except:
                return {
                    "message": "Something went wrong!",
                }, status.HTTP_500_INTERNAL_SERVER_ERROR
            
            from utils.mail import send_email
            token = generate_access_token(new_user)
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

    def account_activate(self, token):
        user = check_access_token(token)
        if user is not None:
            if not user.isActive:
                user.isActive = True
                user.updated = datetime.datetime.now()
                UserServices().save(user)
                
                from utils.mail import send_email
                subject = "Your account is confirmed successfully"
                send_email(user, subject, template='mail/activate_success.html')
                
                return {"status":'success', "message":'You have confirmed your account. Thanks!'}, status.HTTP_200_OK
            else:
                return {"status":'success', "message":'Account already confirmed. Please login.'}, status.HTTP_200_OK
        else:
            return {"status":'fail', "message":'The confirmation link is invalid or has expired.'}, status.HTTP_400_BAD_REQUEST

    def encode_auth_token(self, user):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'publicId': user.publicId,
            'isAdmin': user.isAdmin,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    def decode_auth_token(self, token):
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return UserServices().get_by_publicId(data.sub.publicId)

    def login(self, email, password):
        """Login a user"""
        is_validated = validators.validate_email_and_password(email, password)
        if is_validated is not True:
            return dict(status="fail", message='Invalid data', error=is_validated), status.HTTP_400_BAD_REQUEST
        user = UserServices().get_by_email(email)
        if not user or not user.check_password(password):
            res = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
            return res, status.HTTP_401_UNAUTHORIZED
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

    def refresh_token(self, identity):
        user = UserServices().get_by_publicId(identity['publicId'])
        if user is not None:
            new_access = create_access_token(identity=identity)
            return {"access": new_access}, status.HTTP_200_OK
        return {
                'status': 'fail',
                "message": "The token is invalid or expired",
                "code": "token_not_valid"
            }, status.HTTP_401_UNAUTHORIZED