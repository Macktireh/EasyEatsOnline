from typing import List

from werkzeug import exceptions

from models.user import User
from repositories.userRepository import userRepository
from utils.types import RequestUserUpdateDTO


class UserService:
    @staticmethod
    def getAllUsers(currentUserPublicId: str) -> List[User]:
        return userRepository.getAllUsersExceptCurrent(currentUserPublicId)

    @staticmethod
    def getUser(publicId: str) -> User:
        user: User | None = userRepository.getByPublicId(publicId)
        if not user:
            raise exceptions.NotFound("User not found")
        return user

    @staticmethod
    def updateUser(publicId: str, data: RequestUserUpdateDTO) -> User:
        user = userRepository.getByPublicId(publicId)
        if not user:
            raise exceptions.NotFound("User not found")

        user.firstName = data.get("firstName", user.firstName)
        user.lastName = data.get("lastName", user.lastName)
        return userRepository.save(user)
