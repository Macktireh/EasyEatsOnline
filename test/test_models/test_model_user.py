import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.user import User


class TestUserModel(TestCase):
    
    def create_app(self):
        flask_app.config.from_object('config.settings.TestingConfig')
        return flask_app
    
    def setUp(self):
        db.create_all()
        
        self.user1 = User.create(
            email='user1@example.com',
            firstName='User',
            lastName='One',
            password='password1'
        )
        self.user2 = User.create(
            email='user2@example.com',
            firstName='User',
            lastName='Two',
            password='password2'
        )
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')

    def test_create_user(self):
        new_user = User.create(
            email='new_user@example.com',
            firstName='New',
            lastName='User',
            password='password'
        )
        self.assertEqual(new_user.email, 'new_user@example.com')
        self.assertEqual(new_user.firstName, 'New')
        self.assertEqual(new_user.lastName, 'User')
        self.assertTrue(new_user.checkPassword('password'))

    def test_create_superuser(self):
        new_superuser = User.createSuperUser(
            email='new_superuser@example.com',
            firstName='New',
            lastName='Superuser',
            password='password'
        )
        self.assertEqual(new_superuser.email, 'new_superuser@example.com')
        self.assertEqual(new_superuser.firstName, 'New')
        self.assertEqual(new_superuser.lastName, 'Superuser')
        self.assertTrue(new_superuser.isActive)
        self.assertTrue(new_superuser.isStaff)
        self.assertTrue(new_superuser.isAdmin)
        self.assertTrue(new_superuser.checkPassword('password'))

    def test_check_password(self):
        self.assertTrue(self.user1.checkPassword('password1'))
        self.assertTrue(self.user2.checkPassword('password2'))
        self.assertFalse(self.user1.checkPassword('wrong_password'))
        self.assertFalse(self.user2.checkPassword('wrong_password'))

    def test_get_user_by_public_id(self):
        user = User.getByPublicId(self.user1.publicId)
        self.assertEqual(user.email, 'user1@example.com')
        self.assertEqual(user.firstName, 'User')
        self.assertEqual(user.lastName, 'One')

    def test_get_user_by_email(self):
        user = User.getByEmail(self.user1.email)
        self.assertEqual(user.publicId, self.user1.publicId)
    
    def test_generate_access_token(self):
        token = self.user1.generateAccessToken()
        self.assertIsNotNone(token)
    
    def test_check_access_token(self):
        token = self.user1.generateAccessToken()
        user = User.checkAccessToken(token)
        self.assertEqual(user.publicId, self.user1.publicId)
    
    def test_authenticate(self):
        authenticated_user = User.authenticate(self.user1.email, 'password1')
        self.assertEqual(authenticated_user.email, 'user1@example.com')
        self.assertIsNone(User.authenticate(self.user1.email, 'wrong_password'))
        self.assertIsNone(User.authenticate('wrong_email@example.com', 'password1'))
    
    def test_save_user(self):
        self.user1.email = 'updated_email@example.com'
        self.user1.save()
        updated_user = User.getByPublicId(self.user1.publicId)
        self.assertEqual(updated_user.email, 'updated_email@example.com')
    
    def test_delete_user(self):
        self.user1.delete()
        self.assertIsNone(User.getByPublicId(self.user1.publicId))



if __name__ == '__main__':
    unittest.main()