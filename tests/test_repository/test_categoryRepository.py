import unittest

from flask import Flask
from flask_testing import TestCase

from app import createApp, db
from repository.categoryRepository import categoryRepository


class CategoryRepositoryTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.data = {
            "name": "Test Category",
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_repository_category_create_category(self) -> None:
        category = categoryRepository.create(**self.data)
        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, self.data["name"])

    def test_repository_category_get_all_categories(self) -> None:
        categoryRepository.create(**self.data)
        categoryRepository.create(name="Category 2")
        categories = categoryRepository.getAll()
        self.assertEqual(len(categories), 2)

    def test_repository_category_get_category_by_id(self) -> None:
        category = categoryRepository.create(**self.data)
        retrieved_category = categoryRepository.getById(category.id)
        self.assertIsNotNone(retrieved_category)
        self.assertEqual(retrieved_category.id, category.id)
        self.assertEqual(retrieved_category.name, self.data["name"])

    def test_repository_category_get_category_by_public_id(self) -> None:
        category = categoryRepository.create(**self.data)
        retrieved_category = categoryRepository.getByPublicId(category.publicId)
        self.assertIsNotNone(retrieved_category)
        self.assertEqual(retrieved_category.id, category.id)
        self.assertEqual(retrieved_category.name, self.data["name"])

    def test_repository_category_filter_categories(self) -> None:
        category1 = categoryRepository.create(**self.data)
        categoryRepository.create(name="Category 2")
        filtered_category = categoryRepository.filter(name=self.data["name"])
        self.assertIsNotNone(filtered_category)
        self.assertEqual(filtered_category.id, category1.id)
        self.assertEqual(filtered_category.name, self.data["name"])

    def test_repository_category_filter_all_categories(self) -> None:
        categoryRepository.create(**self.data)
        categoryRepository.create(name="Category 2")
        filtered_categories = categoryRepository.filterAll(name=self.data["name"])
        self.assertEqual(len(filtered_categories), 1)

    def test_repository_category_get_or_create_category(self) -> None:
        category, created = categoryRepository.getOrCreate(**self.data)
        self.assertTrue(created)
        category2, created2 = categoryRepository.getOrCreate(name=self.data["name"])
        self.assertFalse(created2)
        self.assertEqual(category.id, category2.id)

    def test_repository_category_delete_category(self) -> None:
        category = categoryRepository.create(**self.data)
        self.assertIsNotNone(category)
        categoryRepository.delete(category)
        retrieved_category = categoryRepository.getById(category.id)
        self.assertIsNone(retrieved_category)


if __name__ == "__main__":
    unittest.main()
