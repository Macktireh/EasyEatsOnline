import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.user import User
from models.category import Category
from utils import status


class TestCategoryrRoutes(TestCase):
    
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
        
        self.category1 = Category.create(name='Category 1')
        self.category2 = Category.create(name='Category 2')
        self.baseUrl = "http://127.0.0.1:5000/api/categories"
        
        response = self.client.post("http://127.0.0.1:5000/api/auth/user/login", json={ "email": self.user1.email, "password": 'password' })
        self.tokens = response.json['tokens']
        self.headers = {
            'Authorization': f'Bearer {self.tokens.get("access")}'
        }
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_endpoint_list_categories(self):
        response = self.client.get(f"{self.baseUrl}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json['data']), 2)
    
    def test_endpoint_list_categories_not_authenticate(self):
        response = self.client.get(f"{self.baseUrl}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_create_category(self):
        response = self.client.post(f"{self.baseUrl}", json={"name": 'New Category'}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json['name'], 'New Category')
    
    def test_endpoint_create_category_not_authenticate(self):
        response = self.client.post(f"{self.baseUrl}", json={"name": 'New Category'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_get_category_by_publicId(self):
        response = self.client.get(f"{self.baseUrl}/{self.category1.publicId}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_endpoint_get_category_by_publicId_not_authenticate(self):
        response = self.client.get(f"{self.baseUrl}/{self.category1.publicId}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_update_category_by_publicId(self):
        response = self.client.patch(f"{self.baseUrl}/{self.category1.publicId}", json={"name": 'Updated Category 1'}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.category1.name, 'Updated Category 1')
    
    def test_endpoint_update_category_by_publicId_not_authenticate(self):
        response = self.client.patch(f"{self.baseUrl}/{self.category1.publicId}", json={"name": 'Updated Category 1'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_delete_category_by_publicId(self):
        response = self.client.delete(f"{self.baseUrl}/{self.category1.publicId}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_endpoint_delete_category_by_publicId_not_authenticate(self):
        response = self.client.delete(f"{self.baseUrl}/{self.category1.publicId}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()