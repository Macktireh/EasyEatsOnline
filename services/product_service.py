from datetime import datetime
from typing import List, Literal, Dict, Union
from uuid import uuid4
from slugify import slugify

from models.product import Product
from utils import status


class ProductServices:
    def __init__(self) -> None:
        return
    
    @staticmethod
    def create(data) -> Product:
        
        product = Product(
                publicId=str(uuid4()),
                name=data.get('name'),
                slug=slugify(data.get('name')),
                price=float(data.get('price')),
                categoryId=data.get('categoryId'),
                urlImage=data.get('urlImage'),
                description=data.get('description'),
                available=True if data.get('available') else False,
                createdAt=datetime.now(),
                updatedAt=datetime.now(),
            )
        return product.save()
    
    # @staticmethod
    # def create_superuser(data) -> User:
    #     user = User(
    #             publicId=str(uuid4()),
    #             email=data.get('email'),
    #             firstName=data.get('firstName'),
    #             lastName=data.get('lastName'),
    #             password=data.get('password'),
    #             isActive=True,
    #             isStaff=True,
    #             isAdmin=True,
    #             updatedAt=datetime.now(),
    #             createdAt=datetime.now()
    #         )
    #     return user.save()
    
    # @staticmethod
    # def get_by_id(id: int) -> User:
    #     return User.query.filter_by(id=id).first()
    
    # @staticmethod
    # def get_by_publicId(publicId: str) -> User:
    #     return User.query.filter_by(publicId=publicId).first()
    
    # @staticmethod
    # def get_by_email(email: str) -> User:
    #     return User.query.filter_by(email=email).first()
    
    # @staticmethod
    # def get_all_users() -> List[User]:
    #     return User.query.all()
    
    # def update_user_by_publicId(self, data: dict, publicId: str = None) -> Union[tuple[Dict[str, str], Literal[400]], User]:
    #     if not publicId or data is None:
    #         return {
    #             "status": "Fail",
    #             "message": "Missing paramters"
    #         }, status.HTTP_400_BAD_REQUEST
    #     user = self.get_by_publicId(publicId=publicId)
    #     firstName = data.get("firstName", None)
    #     lastName = data.get("lastName", None)
    #     if firstName: 
    #         user.firstName = firstName
    #     if lastName: 
    #         user.lastName = lastName
    #     return user.save()
