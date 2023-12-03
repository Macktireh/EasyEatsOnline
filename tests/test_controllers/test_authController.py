import unittest

from flask import Flask, url_for
from flask_testing import TestCase

from config.app import createApp, db
from services.tokenService import TokenService
from tests.fixture import Fixture
from urls.api import router
from utils import status


class AuthControllerTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        app.register_blueprint(router)
        return app

    def setUp(self) -> None:
        db.create_all()
        self.user1, self.user2 = Fixture.createUsers(2)
        self.data = {
            "email": "test.user@example.com",
            "firstName": "test",
            "lastName": "user",
            "password": "Test@1234",
            "passwordConfirm": "Test@1234",
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_controller_auth_signup_ok(self) -> None:
        response = self.client.post(url_for("api.Auth_signup_controller"), json=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_controller_auth_signup_fail(self) -> None:
        data = self.data
        data["password"] = "Test"
        response = self.client.post(url_for("api.Auth_signup_controller"), json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.data
        data["passwordConfirm"] = "Test"
        response = self.client.post(url_for("api.Auth_signup_controller"), json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.data
        del data["passwordConfirm"]
        response = self.client.post(url_for("api.Auth_signup_controller"), json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.data
        data["email"] = "user@com"
        response = self.client.post(url_for("api.Auth_signup_controller"), json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.data
        data["firstName"] = ""
        response = self.client.post(url_for("api.Auth_signup_controller"), json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_controller_auth_login_ok(self) -> None:
        credentials = {"email": self.user2.email, "password": "password"}
        response = self.client.post(url_for("api.Auth_login_controller"), json=credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_auth_login_fail(self) -> None:
        # wrong password
        credentials = {"email": self.user2.email, "password": "wrongpassword"}
        response = self.client.post(url_for("api.Auth_login_controller"), json=credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # wrong email
        credentials = {"email": "wrongemail", "password": "password"}
        response = self.client.post(url_for("api.Auth_login_controller"), json=credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # account not activated
        credentials = {"email": self.user1.email, "password": "password"}
        response = self.client.post(url_for("api.Auth_login_controller"), json=credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_controller_auth_activation_ok(self) -> None:
        token = TokenService.generate(self.user1)
        response = self.client.post(url_for("api.Auth_activation_controller"), json={"token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_auth_activation_fail(self) -> None:
        response = self.client.post(url_for("api.Auth_activation_controller"), json={"token": "wrongtoken"})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        # account already activated
        token = TokenService.generate(self.user2)
        response = self.client.post(url_for("api.Auth_activation_controller"), json={"token": token})
        self.assertEqual(response.status_code, status.HTTP_410_GONE)

    def test_controller_auth_refresh_token_ok(self) -> None:
        credentials = {"email": self.user2.email, "password": "password"}
        res = self.client.post(url_for("api.Auth_login_controller"), json=credentials)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {res.json["tokens"]["refresh"]}',
        }
        response = self.client.post(url_for("api.Auth_refresh_token_controller"), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_controller_auth_refresh_token_fail(self) -> None:
        response = self.client.post(url_for("api.Auth_refresh_token_controller"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer wrongtoken",
        }
        response = self.client.post(url_for("api.Auth_refresh_token_controller"), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == "__main__":
    unittest.main()
