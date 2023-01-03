import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.user import User
from services.user_service import UserServices
from utils import status


class TestUserRoutes(TestCase):
    
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
        
        self.data = {
            "firstName": "John",
            "lastName": "Doe"
        }
        self.baseUrl = "http://127.0.0.1:5000/api/users"
        
        response = self.client.post("http://127.0.0.1:5000/api/auth/user/login", json={ "email": self.user1.email, "password": 'password' })
        self.tokens = response.json['tokens']
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.tokens.get("access")}'
        }
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_endpoint_list_users(self):
        response = self.client.get(f"{self.baseUrl}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_endpoint_list_users_not_authenticate(self):
        response = self.client.get(f"{self.baseUrl}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_get_current_user(self):
        response = self.client.get(f"{self.baseUrl}/me", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_endpoint_get_current_user_not_authenticate(self):
        response = self.client.get(f"{self.baseUrl}/me")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_update_current_user(self):
        response = self.client.patch(f"{self.baseUrl}/me", json=self.data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.firstName, self.data['firstName'])
        self.assertEqual(self.user1.lastName, self.data['lastName'])
    
    def test_endpoint_update_current_user_not_authenticate(self):
        response = self.client.patch(f"{self.baseUrl}/me", json={"firstName": "Hello", "lastName": "World"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



if __name__ == '__main__':
    unittest.main()