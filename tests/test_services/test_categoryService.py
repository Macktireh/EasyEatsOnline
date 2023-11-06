import unittest

from flask import Flask
from flask_testing import TestCase
from werkzeug import exceptions

from app import createApp, db
from services.categoryService import CategoryService
from tests.fixture import Fixture


class CategoryServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.category1, self.category2 = Fixture.createCategories(2)
        self.data = {"name": "Test"}

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_service_category_getAllCategories(self) -> None:
        categories = CategoryService.getAllCategories()
        self.assertEqual(len(categories), 2)

    def test_service_category_addCategory(self) -> None:
        category = CategoryService.addCategory(self.data)
        self.assertEqual(category.name, self.data["name"])
        self.assertEqual(len(CategoryService.getAllCategories()), 3)

        # We check that the category exists in the database
        with self.assertRaises(exceptions.Conflict):
            CategoryService.addCategory(self.data)

        # We check that the category name cannot be empty
        with self.assertRaises(exceptions.BadRequest):
            CategoryService.addCategory({"name": ""})

    def test_service_category_getCategory(self) -> None:
        category = CategoryService.getCategory(self.category1.publicId)
        self.assertEqual(category.name, self.category1.name)

    def test_service_category_updateCategory(self) -> None:
        category = CategoryService.updateCategory(self.category1.publicId, self.data)
        self.assertEqual(category.name, self.data["name"])

    def test_service_category_deleteCategory(self) -> None:
        CategoryService.deleteCategory(self.category1.publicId)
        self.assertEqual(len(CategoryService.getAllCategories()), 1)
        with self.assertRaises(exceptions.NotFound):
            CategoryService.getCategory(self.category1.publicId)


if __name__ == "__main__":
    unittest.main()
