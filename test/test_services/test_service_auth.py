import os
import unittest

from datetime import datetime, timedelta

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.user import User
from services.auth_service import AuthServices
from utils import status


class TestAuthServices(TestCase):
    
    def create_app(self):
        flask_app.config.from_object('config.settings.TestingConfig')
        return flask_app
    
    def setUp(self):
        db.create_all()
        
        self.user1 = User.create(
            email='test-user-one@example.com',
            firstName='User',
            lastName='One',
            password='password'
        )
        self.user1.isActive = True
        self.user1.save()
        
        self.user2 = User.create(
            email='test-user-two@example.com',
            firstName='User',
            lastName='Two',
            password='password'
        )
        
        self.auth_services = AuthServices()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_register(self):
        # Test valid user registration
        data = {
            "email": "new_user@test.com",
            "firstName": "New",
            "lastName": "User",
            "password": "Test@035",
            "passwordConfirm": "Test@035"
        }
        res, status_code = self.auth_services.register(data)
        self.assertEqual(res['message'], 'Successfully registered.')
        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertEqual(res['status'], 'success')
        
        # We check that the user exists in the database
        user = User.getByEmail(data.get('email'))
        self.assertEqual(user.firstName, data.get('firstName'))
        self.assertEqual(user.lastName, data.get('lastName'))
        
        # Test invalid user registration (email already exists)
        res, status_code = self.auth_services.register(data)
        self.assertEqual(status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(res['status'], 'fail')
        self.assertEqual(res['message'], 'User already exists. Please Log in.')
    
    def test_activation(self):
        # Test valid activation
        token = self.user2.generateAccessToken()
        res, status_code = self.auth_services.activation(token)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['message'], 'You have confirmed your account. Thanks!')
        
        # Test invalid activation (token expired)
        self.user1.accessTokenExpiration = datetime.utcnow() - timedelta(hours=1)
        res, status_code = self.auth_services.activation(token)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res['status'], 'fail')
        self.assertEqual(res['message'], 'The confirmation link is invalid or has expired.')
    
    def test_encode_auth_token(self):
        # Test encoding of auth token
        auth_token = self.auth_services.encode_auth_token(self.user1)
        self.assertIsNotNone(auth_token)
    
    def test_decode_auth_token(self):
        # Test decoding of auth token
        auth_token = self.auth_services.encode_auth_token(self.user1)
        decoded_user = self.auth_services.decode_auth_token(auth_token)
        self.assertEqual(decoded_user.publicId, self.user1.publicId)
    
    # Test methods AuthService.login
    def test_login(self):
        # Test valid login
        res, status_code = self.auth_services.login(self.user1.email, 'password')
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['message'], 'Successfully logged in.')
        
        # Test invalid login (the user has not confirmed his account)
        res, status_code = self.auth_services.login(self.user2.email, 'password')
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res['status'], 'fail')
        self.assertEqual(res['message'], 'Please confirm your account!')
        
        # Test invalid login (email does not exist)
        res, status_code = self.auth_services.login('test-user-three@example.com', 'password')
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res['status'], 'fail')
        self.assertEqual(res['message'], 'Invalid email or password.')
    
    # Test methods AuthService.refreshToken
    def test_refreshToken(self):
        # Test valid refresh token
        token1 = self.user1.generateAccessToken()
        identity = self.user1.getJWTIdentity(token1)
        res, status_code = self.auth_services.refreshToken(identity)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['message'], 'Successfully logged in.')



if __name__ == '__main__':
    unittest.main()