import unittest

from flask import Flask, url_for
from flask_testing import TestCase

from config.app import createApp, db
from tests.fixture import Fixture
from urls.api import router
from utils import status


class UserControllerTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        app.register_blueprint(router)
        return app

    def setUp(self) -> None:
        db.create_all()
        self.user1, self.user2 = Fixture.createUsers(2)
        self.credentials = {
            "email": self.user2.email,
            "password": "password",
        }
        res = self.client.post(url_for("api.Auth_login_controller"), json=self.credentials)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {res.json["tokens"]["access"]}',
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_controller_user_list_users_ok(self) -> None:
        response = self.client.get(url_for("api.User_list_user_controller"), headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_user_list_users_fail(self) -> None:
        response = self.client.get(url_for("api.User_list_user_controller"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_controller_user_retrieve_current_user_ok(self) -> None:
        response = self.client.get(
            url_for("api.User_retrieve_update_current_user_controller"),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_user_retrieve_current_user_fail(self) -> None:
        response = self.client.get(url_for("api.User_retrieve_update_current_user_controller"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_controller_user_update_current_user_ok(self) -> None:
        response = self.client.patch(
            url_for("api.User_retrieve_update_current_user_controller"),
            json={"firstName": "Hello", "lastName": "World"},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_user_update_current_user_fail(self) -> None:
        response = self.client.patch(
            url_for("api.User_retrieve_update_current_user_controller"),
            json={"firstName": "Hello", "lastName": "World"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    unittest.main()
