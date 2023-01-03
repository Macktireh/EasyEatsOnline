import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.category import Category
from models.product import Product
from services.product_service import ProductServices
from utils import status


class TestProductServices(TestCase):
    
    def create_app(self):
        flask_app.config.from_object('config.settings.TestingConfig')
        return flask_app
    
    def setUp(self):
        db.create_all()
        
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
        self.product3 = Product.create(
            name='Product 3',
            price=30.99,
            categoryId=None,
            image='product3.jpg',
            description='This is product 3',
        )
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_get_all_products(self):
        produsts, status_code = ProductServices.getAllProducts()
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(produsts), 3)
        self.assertEqual(produsts[0].publicId, self.product1.publicId)
        self.assertEqual(produsts[1].publicId, self.product2.publicId)
        self.assertEqual(produsts[2].publicId, self.product3.publicId)
    
    def test_add_product(self):
        data = {
            "name": "Test Product 4",
            "price": 85.99,
            "categoryPublicId": self.category1.publicId,
        }
        res, status_code = ProductServices.addProduct(data)
        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.get('name'), data['name'])
        self.assertEqual(res.get('price'), data['price'])
        self.assertEqual(res.get('category'), self.category1.name)
        
        # We check that the product exists in the database
        produsts, status_code = ProductServices.getAllProducts()
        self.assertEqual(len(produsts), 4)
        self.assertEqual(produsts[3].publicId, res.get('publicId'))
    
    def test_get_product_by_publicId(self):
        res, status_code = ProductServices.getProductByPublicId(self.product1.publicId)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('publicId'), self.product1.publicId)
        self.assertEqual(res.get('name'), self.product1.name)
        self.assertEqual(res.get('price'), self.product1.price)
    
    def test_update_product_by_publicId(self):
        data = {
            "name": "Updated Product 1",
            "price": 9999.99,
            "categoryPublicId": self.category2.publicId,
        }
        res, status_code = ProductServices.updateProductByPublicId(self.product1.publicId, data)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('publicId'), self.product1.publicId)
        self.assertEqual(res.get('name'), data['name'])
        self.assertEqual(res.get('price'), data['price'])
        self.assertEqual(res.get('category'), self.category2.name)
    
    def test_delete_product_by_publicId(self):
        _, status_code = ProductServices.deleteProductByPublicId(self.product1.publicId)
        self.assertEqual(status_code, status.HTTP_204_NO_CONTENT)
        
        # We check that the product does not exist in the database
        res, status_code = ProductServices.getProductByPublicId(self.product1.publicId)
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.get('status'), 'Fail')
        self.assertEqual(res.get('message'), 'Product not found')


if __name__ == '__main__':
    unittest.main()