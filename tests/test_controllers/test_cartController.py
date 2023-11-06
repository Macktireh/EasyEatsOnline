import unittest

from flask import Flask, url_for
from flask_testing import TestCase

from app import createApp, db
from controllers import apiRoute
from repository.userRepository import userRepository
from tests.fixture import Fixture
from utils import status


class CartControllerTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        app.register_blueprint(apiRoute)
        return app

    def setUp(self) -> None:
        db.create_all()
        self.product = Fixture.createProducts(1, 1)[0]
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

    def test_controller_cart_retrieve_cart(self) -> None:
        res = self.client.get(url_for("api.Cart_retrieve_or_delete_all_from_cart"), headers=self.headersActive)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_controller_cart_retrieve_cart_fail(self) -> None:
        res = self.client.get(url_for("api.Cart_retrieve_or_delete_all_from_cart"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_controller_cart_delete_all_orders_in_cart_ok(self) -> None:
        self.client.get(url_for("api.Cart_retrieve_or_delete_all_from_cart"), headers=self.headersActive)
        res = self.client.delete(url_for("api.Cart_retrieve_or_delete_all_from_cart"), headers=self.headersActive)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_controller_cart_delete_all_orders_in_cart_fail(self) -> None:
        res = self.client.delete(url_for("api.Cart_retrieve_or_delete_all_from_cart"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_controller_cart_add_product_to_cart_ok(self) -> None:
        res = self.client.post(
            url_for("api.Cart_add_to_cart", productPublicId=self.product.publicId), headers=self.headersActive
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_controller_cart_add_product_to_cart_fail(self) -> None:
        # test product not found
        res = self.client.post(
            url_for("api.Cart_add_to_cart", productPublicId="wrongpublicId"), headers=self.headersActive
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # test user is not authenticated
        res = self.client.post(url_for("api.Cart_add_to_cart", productPublicId=self.product.publicId))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_controller_cart_delete_product_from_cart_ok(self) -> None:
        self.client.get(url_for("api.Cart_retrieve_or_delete_all_from_cart"), headers=self.headersActive)
        res = self.client.delete(
            url_for("api.Cart_delete_from_cart", productPublicId=self.product.publicId), headers=self.headersActive
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_controller_cart_delete_product_from_cart_fail(self) -> None:
        # test product not found
        res = self.client.delete(
            url_for("api.Cart_delete_from_cart", productPublicId="wrongpublicId"), headers=self.headersActive
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # test user is not authenticated
        res = self.client.delete(
            url_for("api.Cart_delete_from_cart", productPublicId=self.product.publicId),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    unittest.main()
