import unittest

from flask import Flask, url_for
from flask_testing import TestCase

from app import createApp, db
from controllers import apiRoute
from repository.userRepository import userRepository
from tests.fixture import Fixture
from utils import status


class OrderControllerTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        app.register_blueprint(apiRoute)
        return app

    def setUp(self) -> None:
        db.create_all()
        self.order = Fixture.createOrders(1, 1, 1, 1)[0]
        self.userActive = Fixture.createUsers(1)[0]

        self.userActive.isActive = True
        userRepository.save(self.userActive)

        res = self.client.post(
            url_for("api.Auth_login_controller"), json={"email": self.userActive.email, "password": "password"}
        )
        self.headersActive = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {res.json["tokens"]["access"]}',
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_controller_order_list_orders_ok(self) -> None:
        res = self.client.get(url_for("api.Order_list_order"), headers=self.headersActive)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_controller_order_list_orders_fail(self) -> None:
        res = self.client.get(url_for("api.Order_list_order"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_controller_order_update_quantity_order_ok(self) -> None:
        res = self.client.patch(
            url_for("api.Order_update_quantity_order"),
            json={"publicId": self.order.publicId, "quantity": 2},
            headers=self.headersActive,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_controller_order_update_quantity_order_fail(self) -> None:
        # test order not found
        res = self.client.patch(
            url_for("api.Order_update_quantity_order", publicId="publicId"),
            json={"publicId": "wrongpublicId", "quantity": 2},
            headers=self.headersActive,
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # test quantity > 20
        res = self.client.patch(
            url_for("api.Order_update_quantity_order"),
            json={"publicId": self.order.publicId, "quantity": 21},
            headers=self.headersActive,
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # test quantity < 1
        res = self.client.patch(
            url_for("api.Order_update_quantity_order"),
            json={"publicId": self.order.publicId, "quantity": 0},
            headers=self.headersActive,
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # test user is not authenticated
        res = self.client.patch(
            url_for("api.Order_update_quantity_order"),
            json={"publicId": self.order.publicId, "quantity": 2},
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    unittest.main()
