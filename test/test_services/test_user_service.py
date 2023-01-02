import os
import unittest

from flask_testing import TestCase

from app import db
from manage import flask_app
from models.user import User
from services.user_service import UserServices
from utils import status


class TestUserServices(TestCase):
    
    def create_app(self):
        flask_app.config.from_object('config.settings.TestingConfig')
        return flask_app
    
    def setUp(self):
        db.create_all()
        
        self.user1 = User.create(
            email='test-user-one@example.com',
            firstName='User',
            lastName='One',
            password='password'
        )
        self.user1.isActive = True
        self.user1.save()
        
        self.user2 = User.create(
            email='test-user-two@example.com',
            firstName='User',
            lastName='Two',
            password='password'
        )
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove('db_test.sqlite3')
    
    def test_get_all_users(self):
        users, status_code = UserServices.getAllUsers()
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].publicId, self.user1.publicId)
        self.assertEqual(users[1].publicId, self.user2.publicId)
    
    def test_get_user_by_publicId(self):
        user, status_code = UserServices.getUserByPubliId(self.user1.publicId)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(user.email, self.user1.email)
        self.assertEqual(user.firstName, self.user1.firstName)
        self.assertEqual(user.lastName, self.user1.lastName)
    
    def test_update_user_by_publicId(self):
        user, status_code = UserServices.getUserByPubliId(self.user1.publicId)
        data = {
            "firstName": "Updated",
            "lastName": "User"
        }
        user, status_code = UserServices.updateUserByPublicId(publicId=user.publicId, data=data)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(user.firstName, 'Updated')
        self.assertEqual(user.lastName, 'User')



if __name__ == '__main__':
    unittest.main()