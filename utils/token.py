from datetime import timedelta
from flask_jwt_extended import create_access_token, decode_token
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app as app

from models.user import User


def generate_access_token(user):
    s = TimedJSONWebSignatureSerializer(app.config.get('SECRET_KEY'), 60*60*24)
    return s.dumps({'publicId': user.publicId, 'isActive': user.isActive}).decode('utf-8')
    # return create_access_token(
    #     identity={'publicId': user.publicId, 'isActive': user.isActive}, 
    #     expires_delta=timedelta(hours=24)
    # )

def check_access_token(token):
    try:
        s = TimedJSONWebSignatureSerializer(app.config.get('SECRET_KEY'), timedelta(hours=24))
        
        # identity = decode_token(token)["sub"]
        identity = s.loads(token)
        user = User.query.filter_by(publicId=identity['publicId']).first()
        # isActive = identity.get('isActive', None)
        # if isActive == True or isActive == False:
        if identity['isActive'] == user.isActive:
            return user
        # isAdmin = identity.get('isAdmin', None)
        # if isAdmin == True or isAdmin == False:
        #     if identity['isAdmin'] == user.isAdmin:
        #         return user
        return None
    except:
        return None