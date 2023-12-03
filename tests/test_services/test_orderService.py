import unittest

from flask import Flask
from flask_testing import TestCase
from werkzeug import exceptions

from config.app import createApp, db
from services.orderService import OrderService
from tests.fixture import Fixture


class OrderServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.nOrders = 1
        self.order = Fixture.createOrders(n=self.nOrders, nUsers=1, nCategories=1, nProducts=1)[0]
        self.data = {
            "publicId": self.order.publicId,
            "quantity": 10,
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_service_order_getAllOrders(self) -> None:
        orders = OrderService.getAllOrders()
        self.assertEqual(len(orders), self.nOrders)

    def test_service_order_updateQuantity(self) -> None:
        order = OrderService.updateQuantity(self.data)
        self.assertEqual(order.quantity, self.data["quantity"])

        with self.assertRaises(exceptions.BadRequest):
            OrderService.updateQuantity({"publicId": self.order.publicId, "quantity": 0})

        with self.assertRaises(exceptions.BadRequest):
            OrderService.updateQuantity({"publicId": self.order.publicId, "quantity": 21})

        with self.assertRaises(exceptions.BadRequest):
            OrderService.updateQuantity({"publicId": self.order.publicId, "quantity": "21"})

        with self.assertRaises(exceptions.NotFound):
            OrderService.updateQuantity({"publicId": "invalid", "quantity": 10})


if __name__ == "__main__":
    unittest.main()
