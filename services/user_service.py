import uuid
import datetime

from typing import List, Literal, Dict, Union
from werkzeug.utils import secure_filename

from app import db
from models.user import User, UserImage
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
    
    def update_user_by_publicId(self, data: dict, publicId: str = None) -> Union[tuple[Dict[str, str], Literal[400]], User]:
        if not publicId or data is None:
            return {
                "status": "Fail",
                "message": "Missing paramters"
            }, status.HTTP_400_BAD_REQUEST
        user = self.get_by_publicId(publicId=publicId)
        firstName = data.get("firstName", None)
        lastName = data.get("lastName", None)
        if firstName: 
            user.firstName = firstName
        if lastName: 
            user.lastName = lastName
        return self.save(user)
    
    def upload_image(self, publicId: str, image) -> Union[tuple[dict[str, str], Literal[400]], tuple[dict[str, str], Literal[200]]]:
        if not publicId or not image:
            return {
                "status": "Fail",
                "message": "Missing paramters"
            }, status.HTTP_400_BAD_REQUEST
        
        user = self.get_by_publicId(publicId=publicId)
        fileName = secure_filename(image.filename)
        minetype = image.mimetype
        if not user.image:
            user.image = UserImage(image=image.read(), name=fileName, nimeType=minetype, publicId=user.publicId)
        else:
            user.image.image = image.read()
            user.image.name=fileName
            user.image.nimeType=minetype
        self.save(user)
        
        return {
            "status": "Success",
            "message": "Image uploaded successfully"
        }, status.HTTP_200_OK
    
    def save(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
