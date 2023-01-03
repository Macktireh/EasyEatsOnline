import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.category import Category
from services.category_service import CategoryServices
from utils import status


class TestCategoryServices(TestCase):
    
    def create_app(self):
        flask_app.config.from_object('config.settings.TestingConfig')
        return flask_app
    
    def setUp(self):
        db.create_all()
        
        self.category1 = Category.create(name='Category 1')
        self.category2 = Category.create(name='Category 2')
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_get_all_categories(self):
        categories, status_code = CategoryServices.getAllCategories()
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0].publicId, self.category1.publicId)
        self.assertEqual(categories[1].publicId, self.category2.publicId)
    
    def test_add_category(self):
        data = {"name": "Test Category 3"}
        res, status_code = CategoryServices.addCategory(data)
        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.get('name'), data['name'])
        
        # We check that the category exists in the database
        categories, status_code = CategoryServices.getAllCategories()
        self.assertEqual(len(categories), 3)
        self.assertEqual(categories[2].publicId, res.get('publicId'))
    
    def test_get_category_by_publicId(self):
        res, status_code = CategoryServices.getCategoryByPublicId(self.category1.publicId)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('publicId'), self.category1.publicId)
        self.assertEqual(res.get('name'), self.category1.name)
    
    def test_update_category_by_publicId(self):
        data = {"name": "Updated Category 1"}
        res, status_code = CategoryServices.updateCategoryByPublicId(publicId=self.category1.publicId, data=data)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('publicId'), self.category1.publicId)
        self.assertEqual(res.get('name'), data['name'])
    
    def test_delete_category_by_publicId(self):
        _, status_code = CategoryServices.deleteCategoryByPublicId(self.category1.publicId)
        self.assertEqual(status_code, status.HTTP_204_NO_CONTENT)
        
        # We check that the category does not exist in the database
        res, status_code = CategoryServices.getCategoryByPublicId(self.category1.publicId)
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.get('status'), 'Fail')
        self.assertEqual(res.get('message'), 'Category not found')


if __name__ == '__main__':
    unittest.main()