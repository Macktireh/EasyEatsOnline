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
            categoryId=self.category1.id,
            image='product3.jpg',
            description='This is product 3',
        )
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_get_category_all(self):
        categories = Category.getAll()
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0].publicId, self.category1.publicId)
        self.assertEqual(categories[1].publicId, self.category2.publicId)
    
    def test_get_all_category_by_name(self):
        categories = Category.getAllByName('Category 1')
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].publicId, self.category1.publicId)
    
    def test_to_dict_category(self):
        category_dict = self.category1.toDict()
        self.assertEqual(category_dict['publicId'], self.category1.publicId)
        self.assertEqual(category_dict['name'], 'Category 1')
        self.assertEqual(category_dict['createdAt'], self.category1.createdAt.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(category_dict['updatedAt'], self.category1.updatedAt.strftime("%Y-%m-%d %H:%M:%S"))
    
    def test_to_dict_with_products(self):
        category_dict = self.category1.toDictWithProducts()
        self.assertEqual(category_dict['publicId'], self.category1.publicId)
        self.assertEqual(category_dict['name'], 'Category 1')
        self.assertEqual(category_dict['createdAt'], self.category1.createdAt.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(category_dict['updatedAt'], self.category1.updatedAt.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(len(category_dict['products']), 2)
        self.assertEqual(category_dict['products'][0]['publicId'], self.product1.publicId)
        self.assertEqual(category_dict['products'][1]['publicId'], self.product3.publicId)
    
    def test_delete_category(self):
        self.category1.delete()
        self.assertIsNone(Category.getById(self.category1.id))
        self.assertIsNone(Category.getByPublicId(self.category1.publicId))




if __name__ == '__main__':
    unittest.main()