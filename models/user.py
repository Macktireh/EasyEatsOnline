from typing import List, NoReturn, Union
from datetime import datetime, timedelta
from uuid import uuid4
from itsdangerous import TimedJSONWebSignatureSerializer

from flask_login import UserMixin
from flask import current_app as app

from app import db, flask_bcrypt


class User(db.Model, UserMixin):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstName = db.Column(db.String(128), nullable=False)
    lastName = db.Column(db.String(128), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=False)
    isStaff = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)
    passwordHash = db.Column(db.Text, nullable=False)
    
    @property
    def password(self) -> NoReturn:
        raise AttributeError('password: write-only field')
    
    @password.setter
    def password(self, password: str) -> None:
        self.passwordHash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    
    def checkPassword(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.passwordHash, password)
    
    def generateAccessToken(self) -> str:
        s = TimedJSONWebSignatureSerializer(app.config.get('SECRET_KEY'), 60*60*24)
        return s.dumps({'publicId': self.publicId, 'isActive': self.isActive}).decode('utf-8')
    
    @classmethod
    def checkAccessToken(cls, token: str) -> Union["User", None]:
        try:
            s = TimedJSONWebSignatureSerializer(app.config.get('SECRET_KEY'), timedelta(hours=24))
            identity = s.loads(token)
            user = cls.getByPublicId(identity['publicId'])
            if identity['isActive'] == user.isActive:
                return user
            return None
        except:
            return None
    
    def save(self) -> "User":
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def create(cls, email: str, firstName: str, lastName: str, password: str) -> "User":
        user = cls(
            publicId=str(uuid4()),
            email=email,
            firstName=firstName,
            lastName=lastName,
            password=password,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        return user.save()
    
    @classmethod
    def createSuperUser(cls, email: str, firstName: str, lastName: str, password: str) -> "User":
        user = cls(
            publicId=str(uuid4()),
            email=email,
            firstName=firstName,
            lastName=lastName,
            password=password,
            isActive=True,
            isStaff=True,
            isAdmin=True,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        return user.save()
    
    def delete(self) -> "User":
        db.session.delete(self)
        db.session.commit()
        return self
    
    @classmethod
    def authenticate(cls, email: str, password: str) -> Union["User", None]:
        user = cls.getByEmail(email=email)
        if user and user.checkPassword(password):
            return user
        return None
    
    @classmethod
    def getById(cls, id: int) -> "User":
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getByPublicId(cls, publicId: str) -> "User":
        return cls.query.filter_by(publicId=publicId).first()
    
    @classmethod
    def getByEmail(cls, email: str) -> "User":
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def getAll(cls) -> List["User"]:
        return cls.query.all()
    
    def __repr__(self) -> str:
        return "<User '{}'>".format(self.email)