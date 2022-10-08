from datetime import datetime

from flask_login import UserMixin

from app import db, flask_bcrypt


class User(db.Model, UserMixin):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    isActive = db.Column(db.Boolean, nullable=False, default=False)
    isStaff = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    passwordHash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password: str):
        self.passwordHash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.passwordHash, password)

    def get_full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def __repr__(self):
        return "<User '{}'>".format(self.email)