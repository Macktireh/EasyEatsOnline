from typing import List, Literal, Dict, Tuple, Union

from models.user import User
from utils import status


class UserServices:
    
    @staticmethod
    def getAllUsers() -> Tuple[List[User], Literal[200]]:
        return User.getAll(), status.HTTP_200_OK
    
    @staticmethod
    def getUserByPubliId(publicId: int):
        if not publicId:
            return {
                "status": "Fail",
                "message": "Missing Authorization Header"
            }, status.HTTP_400_BAD_REQUEST
        
        user = User.getByPublicId(publicId)
        if not user:
            return {
                "status": "Fail",
                "message": "User not found"
            }, status.HTTP_404_NOT_FOUND
        return user, status.HTTP_200_OK
    
    @staticmethod
    def updateUserByPublicId(publicId: str, data: dict) -> Union[Tuple[Dict[str, str], Literal[400]], User]:
        if not publicId or data is None:
            return {
                "status": "Fail",
                "message": "Missing paramters"
            }, status.HTTP_400_BAD_REQUEST
        
        user = User.getByPublicId(publicId=publicId)
        firstName = data.get("firstName", None)
        lastName = data.get("lastName", None)
        
        if firstName: 
            user.firstName = firstName
        if lastName: 
            user.lastName = lastName
        return user.save(), status.HTTP_200_OK