import unittest

from flask import Flask
from flask_testing import TestCase

from config.app import createApp, db
from services.tokenService import TokenService
from tests.fixture import Fixture


class TokenServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()

        self.user = Fixture.createUsers(1)[0]

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_service_token_generate(self) -> None:
        _payload = {"publicId": self.user.publicId, "isActive": self.user.isActive}
        token = TokenService.generate(_payload)
        self.assertIsNotNone(token)

    def test_service_token_verify(self) -> None:
        _payload = {"publicId": self.user.publicId, "isActive": self.user.isActive}
        token = TokenService.generate(_payload)
        user = TokenService.verify(token)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user.id)

    def test_service_token_verify_invalid(self) -> None:
        _payload = {"publicId": self.user.publicId, "isActive": self.user.isActive}
        token = TokenService.generate(_payload)
        token = token[:-1]
        user = TokenService.verify(token)
        self.assertIsNone(user)

    def test_service_token_getPayload(self) -> None:
        _payload = {"publicId": self.user.publicId, "isActive": self.user.isActive}
        token = TokenService.generate(_payload)
        payload = TokenService.getPayload(token, 60 * 60 * 24)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["publicId"], self.user.publicId)


if __name__ == "__main__":
    unittest.main()
