import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.user import User
from utils import status


class TestAuthRoutes(TestCase):
    def create_app(self):
        flask_app.config.from_object("config.settings.TestingConfig")
        return flask_app

    def setUp(self):
        db.create_all()

        self.user1 = User.create(
            email="test-user-one@example.com",
            firstName="User",
            lastName="One",
            password="password",
        )
        self.user1.isActive = True
        self.user1.save()

        self.user2 = User.create(
            email="test-user-two@example.com",
            firstName="User",
            lastName="Two",
            password="password",
        )

        self.data = {
            "email": "user-test@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "password": "Test@123",
            "passwordConfirm": "Test@123",
            "sendMail": False,
        }
        self.baseUrl = "http://127.0.0.1:5000/api/auth/user"

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("db_test.sqlite3")

    def test_endpoint_signup(self):
        response = self.client.post(f"{self.baseUrl}/signup", json=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["message"], "User successfully created.")

    def test_endpoint_signup_with_invalid_data_user_already_exists(self):
        payload = self.data.copy()
        payload["email"] = "test-user-one@example.com"
        response = self.client.post(f"{self.baseUrl}/signup", json=payload)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json["status"], "Fail")
        self.assertEqual(
            response.json["message"], "User already exists. Please Log in."
        )

    def test_endpoint_signup_with_invalid_data_password_doesnt_match(self):
        payload = self.data.copy()
        payload["password"] = "Test@123"
        payload["passwordConfirm"] = "Hello@123"
        response = self.client.post(f"{self.baseUrl}/signup", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["status"], "Fail")
        self.assertEqual(
            response.json["message"], "Password and Confirm Password doesn't match."
        )

    def test_endpoint_signup_with_invalid_data_password_is_invalid(self):
        payload = self.data.copy()
        payload["password"] = "Test"
        payload["passwordConfirm"] = "Test"
        response = self.client.post(f"{self.baseUrl}/signup", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["status"], "Fail")
        self.assertEqual(response.json["message"], "Invalid data")
        self.assertEqual(
            response.json["errors"]["password"],
            "Password is invalid, Should be atleast 8 characters with upper and lower case letters, numbers and special characters",
        )

    def test_endpoint_account_activation_success(self):
        payload = {"token": self.user2.generateToken(), "sendMail": False}
        response = self.client.post(f"{self.baseUrl}/account/activation", json=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(
            response.json["message"], "You have confirmed your account. Thanks!"
        )

    def test_endpoint_account_activation_already_activated(self):
        payload = {"token": self.user1.generateToken(), "sendMail": False}
        response = self.client.post(f"{self.baseUrl}/account/activation", json=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(
            response.json["message"], "Account already confirmed. Please login."
        )

    def test_endpoint_account_activation_invalid_token(self):
        payload = {"token": self.user1.generateToken() + "i", "sendMail": False}
        response = self.client.post(f"{self.baseUrl}/account/activation", json=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json["status"], "Fail")
        self.assertEqual(
            response.json["message"], "The confirmation link is invalid or has expired."
        )

    # Test for user login
    def test_endpoint_login_success(self):
        payload = {"email": self.user1.email, "password": "password"}
        response = self.client.post(f"{self.baseUrl}/login", json=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["message"], "Successfully logged in.")

    def test_endpoint_login_non_active_user(self):
        payload = {"email": self.user2.email, "password": "password"}
        response = self.client.post(f"{self.baseUrl}/login", json=payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json["status"], "Fail")
        self.assertEqual(response.json["message"], "Please confirm your account!")

    def test_endpoint_login_invalid_email(self):
        payload = {"email": "invalid-email", "password": "password"}
        response = self.client.post(f"{self.baseUrl}/login", json=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json["status"], "Fail")
        self.assertEqual(response.json["message"], "Invalid email or password.")

    def test_endpoint_login_invalid_password(self):
        payload = {"email": self.user1.email, "password": "invalid-password"}
        response = self.client.post(f"{self.baseUrl}/login", json=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json["status"], "Fail")
        self.assertEqual(response.json["message"], "Invalid email or password.")

    def test_endpoint_refresh_success(self):
        payload = {"email": self.user1.email, "password": "password"}
        response = self.client.post(f"{self.baseUrl}/login", json=payload)
        refresh = response.json["tokens"]["refresh"]
        response = self.client.post(
            f"{self.baseUrl}/token/refresh",
            headers={"Authorization": f"Bearer {refresh}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["message"], "Successfully logged in.")

    def test_endpoint_refresh_invalid_refresh_token(self):
        payload = {"email": self.user1.email, "password": "password"}
        response = self.client.post(f"{self.baseUrl}/login", json=payload)
        refresh = response.json["tokens"]["refresh"] + "j"
        response = self.client.post(
            f"{self.baseUrl}/token/refresh",
            headers={"Authorization": f"Bearer {refresh}"},
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json["msg"], "Signature verification failed")


if __name__ == "__main__":
    unittest.main()
