from typing import Literal, Dict, Tuple, Union

from models.user import User
from utils import status


class UserServices:
    
    @staticmethod
    def updateUser(data: dict, publicId: str = None) -> Union[Tuple[Dict[str, str], Literal[400]], User]:
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
        return user.save()