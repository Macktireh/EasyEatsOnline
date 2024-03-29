import unittest

from flask import Flask
from flask_testing import TestCase
from werkzeug import exceptions

from config.app import createApp, db
from models.product import TypeEnum
from services.productService import ProductService
from tests.fixture import Fixture


class ProductServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.nProducts = 2
        self.product1, self.product2 = Fixture.createProducts(n=self.nProducts, nCategories=2)
        self.data = {
            "name": "Test",
            "price": 14.99,
            "type": TypeEnum.DISH.value.upper(),
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_service_product_getAllProducts(self) -> None:
        products = ProductService.getAllProducts()
        self.assertEqual(len(products), self.nProducts)

    def test_service_product_addProduct(self) -> None:
        product = ProductService.addProduct(self.data)
        self.assertEqual(product.name, self.data["name"])
        self.assertEqual(product.price, self.data["price"])
        self.assertEqual(product.type, TypeEnum.DISH)

        # We check that the product exists in the database
        with self.assertRaises(exceptions.Conflict):
            ProductService.addProduct(self.data)

        # We check that the product name cannot be empty
        with self.assertRaises(exceptions.BadRequest):
            ProductService.addProduct({"name": ""})

    def test_service_product_getProduct(self) -> None:
        product = ProductService.getProduct(self.product1.publicId)
        self.assertEqual(product.name, self.product1.name)

        with self.assertRaises(exceptions.NotFound):
            ProductService.getProduct("invalid")

    def test_service_product_updateProduct(self) -> None:
        product = ProductService.updateProduct(self.product1.publicId, self.data)
        self.assertEqual(product.name, self.data["name"])
        self.assertEqual(product.price, self.data["price"])
        self.assertEqual(product.type, TypeEnum.DISH)

        with self.assertRaises(exceptions.NotFound):
            ProductService.updateProduct("invalid", self.data)

    def test_service_product_deleteProduct(self) -> None:
        ProductService.deleteProduct(self.product1.publicId)
        self.assertEqual(len(ProductService.getAllProducts()), self.nProducts - 1)
        with self.assertRaises(exceptions.NotFound):
            ProductService.getProduct(self.product1.publicId)


if __name__ == "__main__":
    unittest.main()
