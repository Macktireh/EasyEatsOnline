import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.product import Product
from models.user import User
from models.category import Category
from utils import status


class TestProductRoutes(TestCase):
    
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
        self.product1 = Product.create(
            name='Product 1',
            price=10.99,
            categoryId=self.category1.id,
            image='product1.jpg',
            description='This is product 1',
        )
        self.product2 = Product.create(
            name='Product 2',
            price=20.99,
            categoryId=self.category2.id,
            image='product2.jpg',
            description='This is product 2',
        )
        self.baseUrl = "http://127.0.0.1:5000/api/products"
        
        self.data = {
            "name": "Hello World",
            "price": 9999.99,
            "categoryPublicId": self.category2.publicId,
        }
        
        response = self.client.post("http://127.0.0.1:5000/api/auth/user/login", json={ "email": self.user1.email, "password": 'password' })
        self.tokens = response.json['tokens']
        self.headers = {
            'Authorization': f'Bearer {self.tokens.get("access")}'
        }
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_endpoint_list_products(self):
        response = self.client.get(f"{self.baseUrl}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json['data']), 2)
    
    def test_endpoint_list_products_not_authenticate(self):
        response = self.client.get(f"{self.baseUrl}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_create_category(self):
        response = self.client.post(f"{self.baseUrl}", json=self.data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json['name'], self.data['name'])
        self.assertEqual(response.json['price'], self.data['price'])
        self.assertEqual(response.json['category'], self.category2.name)
    
    def test_endpoint_create_product_not_authenticate(self):
        response = self.client.post(f"{self.baseUrl}", json=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_get_product_by_publicId(self):
        response = self.client.get(f"{self.baseUrl}/{self.product1.publicId}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_endpoint_get_product_by_publicId_not_authenticate(self):
        response = self.client.get(f"{self.baseUrl}/{self.product1.publicId}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_update_product_by_publicId(self):
        response = self.client.patch(f"{self.baseUrl}/{self.product1.publicId}", json=self.data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product1.name, self.data['name'])
    
    def test_endpoint_update_product_by_publicId_not_authenticate(self):
        response = self.client.patch(f"{self.baseUrl}/{self.product1.publicId}", json={"name": 'Updated Product 1'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_endpoint_delete_product_by_publicId(self):
        response = self.client.delete(f"{self.baseUrl}/{self.product1.publicId}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_endpoint_delete_product_by_publicId_not_authenticate(self):
        response = self.client.delete(f"{self.baseUrl}/{self.product1.publicId}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()