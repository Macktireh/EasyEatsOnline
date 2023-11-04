import unittest

from flask import Flask
from flask_testing import TestCase

from app import createApp, db
from repository.userRepository import userRepository


class UserRepositoryTestCase(TestCase):

    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        db.create_all()
        self.data = {
            "email": "john.doe@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "password": "password",
        }

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_repository_user_create_user(self) -> None:
        user = userRepository.create(**self.data)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, self.data["email"])
        self.assertFalse(user.isActive)
        self.assertFalse(user.isStaff)
        self.assertFalse(user.isAdmin)

    def test_repository_user_create_super_user(self) -> None:
        super_user = userRepository.createSuperUser(**self.data)
        self.assertIsNotNone(super_user.id)
        self.assertEqual(super_user.email, self.data["email"])
        self.assertTrue(super_user.isActive)
        self.assertTrue(super_user.isAdmin)
        self.assertTrue(super_user.isStaff)

    def test_repository_user_get_all_users(self) -> None:
        user1 = userRepository.create(**self.data)
        user2 = userRepository.create(
            email="user2@example.com",
            firstName="User",
            lastName="Two",
            password="password2",
        )
        users = userRepository.getAll()
        self.assertEqual(len(users), 2)

    def test_repository_user_get_user_by_id(self) -> None:
        user = userRepository.create(**self.data)
        retrieved_user = userRepository.getById(user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)

    def test_repository_user_get_user_by_public_id(self) -> None:
        user = userRepository.create(**self.data)
        retrieved_user = userRepository.getByPublicId(user.publicId)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)

    def test_repository_user_get_user_by_email(self) -> None:
        user = userRepository.create(**self.data)
        retrieved_user = userRepository.getByEmail(user.email)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)

    def test_repository_user_filter_users(self) -> None:
        user = userRepository.create(**self.data)
        retrieved_user = userRepository.filter(email=self.data["email"])
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)

    def test_repository_user_filter_all_users(self) -> None:
        user1 = userRepository.create(**self.data)
        user2 = userRepository.create(
            email="user2@example.com",
            firstName="User",
            lastName="Two",
            password="password2",
        )
        users = userRepository.filterAll(isActive=True)
        self.assertEqual(len(users), 0)

    def test_repository_user_get_or_create_user(self) -> None:
        user, created = userRepository.getOrCreate(**self.data)
        self.assertTrue(created)
        user2, created2 = userRepository.getOrCreate(email=self.data["email"])
        self.assertFalse(created2)
        self.assertEqual(user.id, user2.id)

    def test_repository_user_delete_user(self) -> None:
        user = userRepository.create(**self.data)
        self.assertIsNotNone(user)
        userRepository.delete(user)
        retrieved_user = userRepository.getById(user.id)
        self.assertIsNone(retrieved_user)


if __name__ == "__main__":
    unittest.main()
