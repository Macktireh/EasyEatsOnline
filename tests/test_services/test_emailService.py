import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from flask import Flask
from flask_testing import TestCase

from app import createApp
from services.emailService import EmailService, EmailServiceSettings


class EmailServiceTestCase(TestCase):
    def create_app(self) -> Flask:
        app = createApp("testing")
        return app

    def setUp(self) -> None:
        self.data = {
            "username": "test@test.com",
            "password": "password",
            "server": "smtp.test.com",
            "port": 587,
        }

    def test_service_email_initialization(self) -> None:
        settings = EmailServiceSettings(**self.data)
        email_service = EmailService(settings)

        self.assertEqual(email_service.username, self.data["username"])
        self.assertEqual(email_service.password, self.data["password"])
        self.assertEqual(email_service.server, self.data["server"])
        self.assertEqual(email_service.port, self.data["port"])
        self.assertIsInstance(email_service._msg, MIMEMultipart)

    def test_service_email_subject(self) -> None:
        settings = EmailServiceSettings(**self.data)
        email_service = EmailService(settings)
        email_service.subject("Test Subject")

        self.assertEqual(email_service._subject, "Test Subject")

    def test_service_email_body(self) -> None:
        settings = EmailServiceSettings(**self.data)
        email_service = EmailService(settings)
        email_service.body("Test Body")

        self.assertIsInstance(email_service._msg_body, MIMEText)
        self.assertEqual(email_service._msg_body.get_payload(), "Test Body")

    # def test_service_email_reply_to(self):
    #     settings = EmailServiceSettings(
    #         username="test@test.com",
    #         password="password",
    #         server="smtp.test.com",
    #         port=587,
    #     )
    #     email_service = EmailService(settings)
    #     email_service.reply_to("reply@test.com")

    #     self.assertEqual(email_service._reply_to, "reply@test.com")

    def test_service_email_attach_file(self) -> None:
        settings = EmailServiceSettings(**self.data)
        email_service = EmailService(settings)
        email_service.attach_file(Path("test.txt"))

        self.assertEqual(len(email_service._attachments), 1)

    def test_service_email_send_email(self) -> None:
        settings = EmailServiceSettings(**self.data, dev_mode=True)
        email_service = EmailService(settings)

        email_service.recipients(["test@test.com"])
        result = email_service.send()

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
