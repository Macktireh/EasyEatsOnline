import unittest

from flask import Flask
from flask_testing import TestCase

from config.app import createApp, db
from repositories.orderRepository import orderRepository
from tests.fixture import Fixture


class OrderRepositoryTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()

        self.user1, self.user2 = Fixture.createUsers(2)
        self.product = Fixture.createProducts(1, 1)[0]

        self.data = {
            "userId": self.user1.id,
            "productId": self.product.id,
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_repository_order_create_order(self) -> None:
        order = orderRepository.create(**self.data)
        self.assertIsNotNone(order.id)
        self.assertEqual(order.userId, self.data["userId"])
        self.assertEqual(order.productId, self.data["productId"])
        self.assertEqual(order.quantity, 1)
        self.assertFalse(order.ordered)

    def test_repository_order_get_all_orders(self) -> None:
        orderRepository.create(**self.data)
        orderRepository.create(
            userId=self.user2.id,
            productId=self.product.id,
            quantity=3,
            ordered=True,
        )
        orders = orderRepository.getAll()
        self.assertEqual(len(orders), 2)

    def test_repository_order_get_order_by_id(self) -> None:
        order = orderRepository.create(**self.data)
        retrieved_order = orderRepository.getById(order.id)
        self.assertIsNotNone(retrieved_order)
        self.assertEqual(retrieved_order.id, order.id)

    def test_repository_order_get_order_by_public_id(self) -> None:
        order = orderRepository.create(**self.data)
        retrieved_order = orderRepository.getByPublicId(order.publicId)
        self.assertIsNotNone(retrieved_order)
        self.assertEqual(retrieved_order.id, order.id)

    def test_repository_order_filter_orders(self) -> None:
        order1 = orderRepository.create(**self.data)
        orderRepository.create(
            userId=self.user2.id,
            productId=self.product.id,
            quantity=3,
            ordered=True,
        )
        filtered_order = orderRepository.filter(userId=self.data["userId"])
        self.assertIsNotNone(filtered_order)
        self.assertEqual(filtered_order.id, order1.id)

    def test_repository_order_filter_all_orders(self) -> None:
        orderRepository.create(**self.data)
        orderRepository.create(
            userId=self.user2.id,
            productId=self.product.id,
            quantity=4,
            ordered=True,
        )
        filtered_orders = orderRepository.filterAll(userId=self.data["userId"])
        self.assertEqual(len(filtered_orders), 1)

    def test_repository_order_get_or_create_order(self) -> None:
        order, created = orderRepository.getOrCreate(**self.data)
        self.assertTrue(created)
        order2, created2 = orderRepository.getOrCreate(**self.data)
        self.assertFalse(created2)
        self.assertEqual(order.id, order2.id)

    def test_repository_order_delete_order(self) -> None:
        order = orderRepository.create(**self.data)
        self.assertIsNotNone(order)
        orderRepository.delete(order)
        retrieved_order = orderRepository.getById(order.id)
        self.assertIsNone(retrieved_order)


if __name__ == "__main__":
    unittest.main()
