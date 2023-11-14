from typing import NoReturn

from flask_login import UserMixin

from config.app import db, flask_bcrypt
from models import BaseModel


class User(UserMixin, BaseModel):
    __tablename__ = "user"

    email = db.Column(db.String(255), unique=True, nullable=False)
    firstName = db.Column(db.String(128), nullable=False)
    lastName = db.Column(db.String(128), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=False)
    isStaff = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    passwordHash = db.Column(db.Text, nullable=False)

    @property
    def name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    @property
    def password(self) -> NoReturn:
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str) -> None:
        self.passwordHash = flask_bcrypt.generate_password_hash(password).decode("utf-8")

    def checkPassword(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.passwordHash, password)

    def __repr__(self) -> str:
        return f"<User '{self.email}'>"
