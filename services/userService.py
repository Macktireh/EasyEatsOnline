from typing import List

from models.user import User
from repositories.userRepository import userRepository
from utils.types import RequestUserUpdateDTO


class UserService:
    @staticmethod
    def getAllUsers(currentUserPublicId: str) -> List[User]:
        return userRepository.getAllUsersExceptCurrent(currentUserPublicId)

    @staticmethod
    def getUser(publicId: str) -> User:
        return userRepository.getOr404(publicId=publicId)

    @staticmethod
    def updateUser(publicId: str, data: RequestUserUpdateDTO) -> User:
        user = userRepository.getOr404(publicId=publicId)

        user.firstName = data.get("firstName", user.firstName)
        user.lastName = data.get("lastName", user.lastName)
        return userRepository.save(user)
