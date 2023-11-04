import unittest

from flask import Flask
from flask_testing import TestCase

from app import createApp, db
from models.product import TypeEnum
from repository.productRepository import productRepository


class ProductRepositoryTestCase(TestCase):

    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.data = {
            "name": "Test Product",
            "price": 11.99,
            "type": TypeEnum.DISH,
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_repository_product_create_product(self) -> None:
        product = productRepository.create(**self.data)
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, self.data["name"])
        self.assertEqual(product.price, self.data["price"])
        self.assertEqual(product.type, self.data["type"])

    def test_repository_product_get_all_products(self) -> None:
        product1 = productRepository.create(**self.data)
        product2 = productRepository.create(
            name="Another Product",
            price=9.99,
            type=TypeEnum.APPETIZER,
        )
        products = productRepository.getAll()
        self.assertEqual(len(products), 2)

    def test_repository_product_get_product_by_id(self) -> None:
        product = productRepository.create(**self.data)
        retrieved_product = productRepository.getById(product.id)
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.id, product.id)
        self.assertEqual(retrieved_product.name, self.data["name"])
        self.assertEqual(retrieved_product.price, self.data["price"])

    def test_repository_product_get_product_by_public_id(self) -> None:
        product = productRepository.create(**self.data)
        retrieved_product = productRepository.getByPublicId(product.publicId)
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.id, product.id)
        self.assertEqual(retrieved_product.name, self.data["name"])
        self.assertEqual(retrieved_product.price, self.data["price"])

    def test_repository_product_filter_products(self) -> None:
        product1 = productRepository.create(**self.data)
        product2 = productRepository.create(
            name="Another Product",
            price=9.99,
            type=TypeEnum.APPETIZER,
        )
        filtered_product = productRepository.filter(name=self.data["name"])
        self.assertIsNotNone(filtered_product)
        self.assertEqual(filtered_product.id, product1.id)
        self.assertEqual(filtered_product.name, self.data["name"])
        self.assertEqual(filtered_product.price, self.data["price"])

    def test_repository_product_filter_all_products(self) -> None:
        product1 = productRepository.create(**self.data)
        product2 = productRepository.create(
            name="Another Product",
            price=9.99,
            type=TypeEnum.APPETIZER,
        )
        filtered_products = productRepository.filterAll(type=TypeEnum.APPETIZER)
        self.assertEqual(len(filtered_products), 1)

    def test_repository_product_get_or_create_product(self) -> None:
        product, created = productRepository.getOrCreate(**self.data)
        self.assertTrue(created)
        product2, created2 = productRepository.getOrCreate(name=self.data["name"])
        self.assertFalse(created2)
        self.assertEqual(product.id, product2.id)

    def test_repository_product_delete_product(self) -> None:
        product = productRepository.create(**self.data)
        self.assertIsNotNone(product)
        productRepository.delete(product)
        retrieved_product = productRepository.getById(product.id)
        self.assertIsNone(retrieved_product)


if __name__ == "__main__":
    unittest.main()
