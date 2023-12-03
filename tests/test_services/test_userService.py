import unittest

from flask import Flask
from flask_testing import TestCase
from werkzeug import exceptions

from config.app import createApp, db
from services.userService import UserService
from tests.fixture import Fixture


class UserServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.nUsers = 5
        self.user = Fixture.createUsers(self.nUsers)[0]

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_service_user_get_all_users(self) -> None:
        users = UserService.getAllUsers(self.user.publicId)
        self.assertEqual(len(users), self.nUsers - 1)

    def test_service_user_get_user(self) -> None:
        user = UserService.getUser(self.user.publicId)
        self.assertEqual(user.publicId, self.user.publicId)

    def test_service_user_get_user_not_found(self) -> None:
        with self.assertRaises(exceptions.NotFound):
            UserService.getUser("not_found")

    def test_service_user_update_user(self) -> None:
        user = UserService.updateUser(self.user.publicId, {"firstName": "test", "lastName": "test"})
        self.assertEqual(user.firstName, "test")
        self.assertEqual(user.lastName, "test")

    def test_service_user_update_user_not_found(self) -> None:
        with self.assertRaises(exceptions.NotFound):
            UserService.updateUser("not_found", {"firstName": "test", "lastName": "test"})


if __name__ == "__main__":
    unittest.main()
