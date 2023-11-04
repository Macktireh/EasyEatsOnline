import unittest

from flask import Flask
from flask_testing import TestCase
from werkzeug import exceptions

from app import createApp, db
from services.authService import AuthService
from services.tokenService import TokenService
from tests.fixture import Fixture


class AuthServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.user1, self.user2 = Fixture.createUsers(2)
        self.data = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test.user@ex.com",
            "password": "Test@123",
            "passwordConfirm": "Test@123",
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_service_auth_register(self) -> None:
        response = AuthService.register(self.data, withEmail=False)
        self.assertEqual(response["message"], "You have registered successfully.")
        with self.assertRaises(exceptions.Conflict):
            AuthService.register(self.data, withEmail=False)

    def test_service_auth_register_invalid_email(self) -> None:
        self.data["email"] = "test.user"
        with self.assertRaises(exceptions.BadRequest):
            AuthService.register(self.data, withEmail=False)

    def test_service_auth_register_invalid_password(self) -> None:
        self.data["password"] = "Test"
        with self.assertRaises(exceptions.BadRequest):
            AuthService.register(self.data, withEmail=False)

    def test_service_auth_register_invalid_password_confirm(self) -> None:
        self.data["passwordConfirm"] = "Test"
        with self.assertRaises(exceptions.BadRequest):
            AuthService.register(self.data, withEmail=False)

    def test_service_auth_activation(self) -> None:
        token = TokenService.generate(self.user1)
        response = AuthService.activation({"token": token}, withEmail=False)
        self.assertEqual(response["message"], "Account confirmed successfully")

        # test invalid token
        with self.assertRaises(exceptions.UnprocessableEntity):
            AuthService.activation({"token": "token"}, withEmail=False)

        # test already activated
        with self.assertRaises(exceptions.Gone):
            AuthService.activation(
                {"token": TokenService.generate(self.user1)}, withEmail=False
            )

    def test_service_auth_login(self) -> None:
        response = AuthService.login(
            {"email": self.user2.email, "password": "password"}
        )
        self.assertEqual(response["message"], "Successfully logged in.")

        # test user exists but password is wrong
        with self.assertRaises(exceptions.Unauthorized):
            AuthService.login({"email": self.user2.email, "password": "password123"})

        # test user does not exist
        with self.assertRaises(exceptions.Unauthorized):
            AuthService.login({"email": "usernotexist@ex.com", "password": "password"})

    def test_service_auth_authenticate(self) -> None:
        user = AuthService.authenticate(self.user1.email, "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.publicId, self.user1.publicId)

        # test wrong password
        user = AuthService.authenticate(self.user1.email, "password123")
        self.assertIsNone(user)

        # test user does not exist
        user = AuthService.authenticate("usernotexist@ex.com", "password")
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
