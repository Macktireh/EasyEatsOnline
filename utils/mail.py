from flask import render_template, current_app
from flask_mail import Mail, Message
from threading import Thread


app = current_app._get_current_object()
mail = Mail(app)


# class EmailMessage:
#     def __init__(self, user, subject, template, domain=None, token=None):
#         self.user = user
#         self.subject = subject
#         self.template = template
#         self.domain = domain
#         self.token = token
#         self.app = app
    
#     def send_async(self, msg):
#         with self.app.app_context():
#             try:
#                 mail.send(msg)
#             except ConnectionRefusedError:
#                 raise ValueError("[MAIL SERVER] not working")
    
#     def send(self):
#         msg = Message(
#             self.subject,
#             recipients=[self.user.email],
#             html=render_template(self.template, user=self.user, domain=self.domain, token=self.token),
#             sender=app.config['MAIL_DEFAULT_SENDER']
#         )
#         Thread(target=self.send_async, args=(msg)).start()


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise ValueError("[MAIL SERVER] not working")

def send_email(user, subject, template, domain=None, token=None):
    msg = Message(
        subject,
        recipients=[user.email],
        html=render_template(template, user=user, domain=domain, token=token),
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    Thread(target=send_async_email, args=(app, msg)).start()