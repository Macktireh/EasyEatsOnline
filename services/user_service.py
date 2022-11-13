import uuid
import datetime

from typing import List, Literal, Dict

from app import db
from models.user import User
from utils import status


class UserServices:
    def __init__(self) -> None:
        return

    def create(self, data) -> User:
        user = User(
                publicId=str(uuid.uuid4()),
                email=data.get('email'),
                firstName=data.get('firstName'),
                lastName=data.get('lastName'),
                password=data.get('password'),
                updatedAt=datetime.datetime.utcnow()
            )
        return self.save(user)

    def create_superuser(self, data) -> User:
        user = User(
                publicId=str(uuid.uuid4()),
                email=data.get('email'),
                firstName=data.get('firstName'),
                lastName=data.get('lastName'),
                password=data.get('password'),
                isActive=True,
                isStaff=True,
                isAdmin=True,
                updatedAt=datetime.datetime.utcnow()
            )
        return self.save(user)

    def get_by_id(self, id: int) -> User:
        return User.query.filter_by(id=id).first()

    def get_by_publicId(self, publicId: str) -> User:
        return User.query.filter_by(publicId=publicId).first()

    def get_by_email(self, email: str) -> User:
        return User.query.filter_by(email=email).first()

    def get_all_users(self) -> List[User]:
        return User.query.all()
    
    def update_user_by_publicId(self, data: dict, publicId: str = None) -> tuple[Dict[str, str], Literal[400]] | User:
        print()
        print(data)
        print()
        if publicId is None or publicId == "" or data is None:
            return {
                "status": "Fail",
                "message": "Missing paramters"
            }, status.HTTP_400_BAD_REQUEST
        
        user = User.query.filter_by(publicId=publicId).first()
        
        firstName = data.get("firstName", None)
        lastName = data.get("lastName", None)
        # if firstName or lastName: 
        if firstName: user.firstName = firstName
        if lastName: user.lastName = lastName
        return self.save(user)
        return user

    def save(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user