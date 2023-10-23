from typing import Union
from threading import Thread

from flask import render_template, current_app, Flask
from flask_mail import Mail, Message

from models.user import User


app = current_app._get_current_object()
mail = Mail(app)


def send_async_email(app: Flask, msg: Message) -> None:
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise ValueError("[MAIL SERVER] not working")


def send_email(
    user: User,
    subject: str,
    template: str,
    domain: Union[str, None] = None,
    token: Union[str, None] = None,
) -> None:
    msg = Message(
        subject,
        recipients=[user.email],
        html=render_template(template, user=user, domain=domain, token=token),
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    Thread(target=send_async_email, args=(app, msg)).start()
