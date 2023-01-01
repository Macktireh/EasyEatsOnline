from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.dto import AuthDto
from services.auth_service import AuthServices
from utils import status


api = AuthDto.api


@api.route('/signup')
class Signup(Resource):
    
    @api.response(status.HTTP_201_CREATED, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(AuthDto.ISignup, validate=True)
    def post(self):
        """Creates a new User """
        return AuthServices.register(request.json)


@api.route('/account/activation')
class Activation(Resource):
    
    @api.response(status.HTTP_200_OK, 'Account Activation successfully.')
    @api.doc('Account Activation')
    @api.expect(AuthDto.IToken, validate=True)
    def post(self):
        """Account Activation """
        return AuthServices.activation(request.json.get('token'))


@api.route('/login')
class Login(Resource):
    
    @api.response(status.HTTP_200_OK, 'User successfully login.')
    @api.doc('user login')
    @api.expect(AuthDto.ILogin, validate=True)
    def post(self):
        """user login """
        data: dict = request.json
        return AuthServices.login(data.get('email'), data.get('password'))


@api.route('/token/refresh')
class RefreshToken(Resource):
    
    @api.response(status.HTTP_200_OK, 'Refresh Token JWT')
    @api.doc('Refresh Token JWT')
    @jwt_required(refresh=True)
    def post(self):
        """Refresh JWT Token """
        identity = get_jwt_identity()
        return AuthServices.refreshToken(identity)