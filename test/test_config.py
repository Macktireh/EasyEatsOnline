import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import flask_app
from config.settings import BASE_DIR, DevelopmentConfig, TestingConfig


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        flask_app.config.from_object('config.settings.DevelopmentConfig')
        return flask_app

    def test_app_is_development(self):
        self.assertFalse(flask_app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(flask_app.config['DEBUG'])
        self.assertFalse(current_app == None)
        # self.assertTrue(flask_app.config['SQLALCHEMY_DATABASE_URI'] == DevelopmentConfig.SQLALCHEMY_DATABASE_URI)


class TestTestingConfig(TestCase):
    def create_app(self):
        flask_app.config.from_object('config.settings.TestingConfig')
        return flask_app

    def test_app_is_testing(self):
        self.assertFalse(flask_app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(flask_app.config['DEBUG'])
        self.assertTrue(flask_app.config['TESTING'])
        self.assertTrue(flask_app.config['SQLALCHEMY_DATABASE_URI'] == TestingConfig.SQLALCHEMY_DATABASE_URI)


class TestProductionConfig(TestCase):
    def create_app(self):
        flask_app.config.from_object('config.settings.ProductionConfig')
        return flask_app

    def test_app_is_production(self):
        self.assertFalse(flask_app.config['DEBUG'])


if __name__ == '__main__':
    unittest.main()