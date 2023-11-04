import unittest

from flask import Flask
from flask_testing import TestCase
from werkzeug import exceptions

from app import createApp, db
from services.cartService import CartService
from tests.fixture import Fixture


class CartServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.user1, self.user2 = Fixture.createUsers(2)
        self.product1, self.product2 = Fixture.createProducts(2)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_service_cart_addToCart(self) -> None:
        cart = CartService.addToCart(self.user1.publicId, self.product1.publicId)
        self.assertEqual(len(cart.orders), 1)
        self.assertEqual(cart.orders[0].quantity, 1)
        cart = CartService.addToCart(self.user1.publicId, self.product1.publicId)
        self.assertEqual(len(cart.orders), 1)
        self.assertEqual(cart.orders[0].quantity, 2)

    def test_service_cart_retrieveCart(self) -> None:
        for i in range(3):
            CartService.addToCart(self.user1.publicId, self.product1.publicId)
        cart = CartService.retrieveCart(self.user1.publicId)
        self.assertEqual(len(cart.orders), 1)
        self.assertEqual(cart.orders[0].quantity, 3)

    def test_service_cart_deleteFromCart(self) -> None:
        CartService.addToCart(self.user1.publicId, self.product1.publicId)
        cart = CartService.deleteFromCart(self.user1.publicId, self.product1.publicId)
        self.assertEqual(len(cart.orders), 0)

        with self.assertRaises(exceptions.NotFound):
            CartService.deleteFromCart(self.user2.publicId, self.product1.publicId)

    def test_service_cart_deleteAllFromCart(self) -> None:
        for i in range(3):
            CartService.addToCart(self.user1.publicId, self.product1.publicId)
        CartService.deleteAllFromCart(self.user1.publicId)
        cart = CartService.retrieveCart(self.user1.publicId)
        self.assertEqual(len(cart.orders), 0)

        with self.assertRaises(exceptions.NotFound):
            CartService.deleteAllFromCart(self.user2.publicId)


if __name__ == "__main__":
    unittest.main()
