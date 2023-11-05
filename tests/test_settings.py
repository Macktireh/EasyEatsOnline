import unittest

from flask import Flask
from flask_testing import TestCase

from app import createApp
from config.settings import DevelopmentConfig, ProductionConfig, TestingConfig


class TestDevelopmentConfig(TestCase):
    def create_app(self) -> Flask:
        app = createApp("development")
        return app

    def test_app_is_development(self) -> None:
        self.assertNotEqual(self.app.config["SECRET_KEY"], "my_precious")
        self.assertTrue(self.app.config["DEBUG"])
        self.assertEqual(
            self.app.config["SQLALCHEMY_DATABASE_URI"],
            DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
        )


class TestTestingConfig(TestCase):
    def create_app(self) -> Flask:
        # Utilisez ici votre application Flask avec la configuration de test
        self.app = createApp("testing")
        return self.app

    def test_app_is_testing(self) -> None:
        self.assertNotEqual(self.app.config["SECRET_KEY"], "my_precious")
        self.assertTrue(self.app.config["DEBUG"])
        self.assertTrue(self.app.config["TESTING"])
        self.assertEqual(
            self.app.config["SQLALCHEMY_DATABASE_URI"],
            TestingConfig.SQLALCHEMY_DATABASE_URI,
        )


class TestProductionConfig(TestCase):
    def create_app(self) -> Flask:
        # Utilisez ici votre application Flask avec la configuration de test
        app = createApp("production")
        return app

    def test_app_is_production(self) -> None:
        self.assertFalse(self.app.config["DEBUG"])
        self.assertEqual(
            self.app.config["SQLALCHEMY_DATABASE_URI"],
            ProductionConfig.SQLALCHEMY_DATABASE_URI,
        )


if __name__ == "__main__":
    unittest.main()
