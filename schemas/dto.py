from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('Auth', description='user auth')
    ISignup = api.model('signup', {
        'email': fields.String(required=True, description='user email address'),
        'firstName': fields.String(required=True, description='user firstname'),
        'lastName': fields.String(required=True, description='user lastname'),
        'publicId': fields.String(description='user Identifier'),
        'password': fields.String(required=True, description='user password'),
        'passwordConfirm': fields.String(required=True, description='user password confirm'),
    })
    ILogin = api.model('login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })
    IToken = api.model('token', {
        'token': fields.String(required=True, description='token'),
    })

class UserDto:
    api = Namespace('User', description='user related operations')
    IUser = api.model('users', {
        'email': fields.String(required=True, description='user email address'),
        'firstName': fields.String(required=True, description='user firstname'),
        'lastName': fields.String(required=True, description='user lastname'),
        'publicId': fields.String(description='user Identifier'),
    })
    IUserUpdtae = api.model('users', {
        'firstName': fields.String(required=False, description='user firstname'),
        'lastName': fields.String(required=False, description='user lastname'),
    })