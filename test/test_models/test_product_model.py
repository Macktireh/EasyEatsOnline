import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.product import Product
from models.category import Category


class TestProductModel(TestCase):
    
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
    
    def test_create_product(self):
        new_product = Product.create(
            name='New Product',
            price=50.99,
            categoryId=self.category1.id,
            image='new_product.jpg',
            description='This is a new product',
        )
        self.assertEqual(new_product.name, 'New Product')
        self.assertEqual(new_product.price, 50.99)
        self.assertEqual(new_product.categoryId, self.category1.id)
        self.assertEqual(new_product.image, 'new_product.jpg')
        self.assertEqual(new_product.description, 'This is a new product')
        self.assertTrue(new_product.available)
    
    def test_get_product_by_id(self):
        product = Product.getById(self.product1.id)
        self.assertEqual(product.publicId, self.product1.publicId)
        self.assertEqual(product.name, 'Product 1')
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.categoryId, self.category1.id)
        self.assertEqual(product.image, 'product1.jpg')
        self.assertEqual(product.description, 'This is product 1')
    
    def test_get_product_by_publicId(self):
        product = Product.getByPublicId(self.product1.publicId)
        self.assertEqual(product.id, self.product1.id)
        self.assertEqual(product.name, 'Product 1')
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.categoryId, self.category1.id)
    
    def test_get_all_product(self):
        products = Product.getAll()
        self.assertEqual(len(products), 3)
        self.assertEqual(products[0].publicId, self.product1.publicId)
        self.assertEqual(products[1].publicId, self.product2.publicId)
        self.assertEqual(products[2].publicId, self.product3.publicId)
    
    def test_get_all_product_by_name(self):
        products = Product.getAllByName('Product 1')
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].publicId, self.product1.publicId)
    
    def test_to_dict_product(self):
        product_dict = self.product1.toDict()
        self.assertEqual(product_dict['publicId'], self.product1.publicId)
        self.assertEqual(product_dict['name'], 'Product 1')
        self.assertEqual(product_dict['price'], 10.99)
        self.assertEqual(product_dict['category'], 'Category 1')
        self.assertEqual(product_dict['image'], 'product1.jpg')
        self.assertEqual(product_dict['description'], 'This is product 1')
        self.assertTrue(product_dict['available'])
        self.assertEqual(product_dict['createdAt'], self.product1.createdAt.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(product_dict['updatedAt'], self.product1.updatedAt.strftime("%Y-%m-%d %H:%M:%S"))
    
    def test_delete_product(self):
        self.product1.delete()
        self.assertIsNone(Product.getById(self.product1.id))
        self.assertIsNone(Product.getByPublicId(self.product1.publicId))



if __name__ == '__main__':
    unittest.main()